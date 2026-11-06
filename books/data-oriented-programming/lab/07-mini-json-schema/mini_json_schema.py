"""A mini JSON Schema validator: the keywords of DOP chapter 7 in plain Python.

type, properties, required, items, enum, additionalProperties, allOf, anyOf and oneOf,
with Ajv-style errors (instancePath, schemaPath, keyword, message) and an all-errors
switch. Runs the chapter's requests and responses (listings 7.8-7.23, pp. 148-160)
through it. Standard library only; no randomness.
"""
import json

TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}


def type_ok(t, x):
    if t == "integer":
        return isinstance(x, int) and not isinstance(x, bool)
    if t == "number":
        return isinstance(x, (int, float)) and not isinstance(x, bool)
    return isinstance(x, TYPES[t])


def validate(schema, data, all_errors=False):
    errors = []

    def err(path, sp, kw, msg):
        errors.append({"instancePath": path, "schemaPath": sp, "keyword": kw, "message": msg})

    def v(s, d, path, sp):
        start = len(errors)

        def stop():
            return not all_errors and len(errors) > start

        if "type" in s and not type_ok(s["type"], d):
            return err(path, sp + "/type", "type", f"must be {s['type']}")
        if "enum" in s and d not in s["enum"]:
            err(path, sp + "/enum", "enum", "must be equal to one of the allowed values")
            if stop():
                return
        if isinstance(d, dict):
            for k in s.get("required", []):
                if k not in d:
                    err(path, sp + "/required", "required", f"must have required property '{k}'")
                    if stop():
                        return
            for k, x in d.items():
                if k in s.get("properties", {}):
                    v(s["properties"][k], x, f"{path}/{k}", f"{sp}/properties/{k}")
                elif s.get("additionalProperties") is False:
                    err(path, sp + "/additionalProperties", "additionalProperties", "must NOT have additional properties")
                if stop():
                    return
        if isinstance(d, list) and "items" in s:
            for i, x in enumerate(d):
                v(s["items"], x, f"{path}/{i}", sp + "/items")
                if stop():
                    return
        for i, sub in enumerate(s.get("allOf", [])):
            v(sub, d, path, f"{sp}/allOf/{i}")
            if stop():
                return
        for kw in ("anyOf", "oneOf"):
            if kw in s:
                n = sum(1 for sub in s[kw] if not validate(sub, d))
                if kw == "anyOf" and n == 0:
                    err(path, sp + "/anyOf", "anyOf", "must match a schema in anyOf")
                if kw == "oneOf" and n != 1:
                    err(path, sp + "/oneOf", "oneOf", "must match exactly one schema in oneOf")

    v(schema, data, "", "#")
    return errors


def errors_text(errs):
    return ", ".join(f"data{e['instancePath']} {e['message']}" for e in errs)


def report(label, schema, data, all_errors=False):
    errs = validate(schema, data, all_errors)
    print(f"{label:<58} {'valid' if not errs else 'INVALID: ' + errors_text(errs)}")
    return errs


strings = {"type": "array", "items": {"type": "string"}}
search_request = {"type": "object", "properties": {"title": {"type": "string"}, "fields": strings}, "required": ["title", "fields"]}
search_request_enum = {**search_request, "properties": {"title": {"type": "string"}, "fields": {"type": "array", "items": {"enum": [
    "publishers", "number_of_pages", "weight", "physical_format", "subjects", "publish_date", "physical_dimensions"]}}}}
db_book = {"type": "object", "required": ["title", "isbn", "available"],
           "properties": {"title": {"type": "string"}, "available": {"type": "boolean"}, "isbn": {"type": "string"}}}
db_response = {"type": "array", "items": db_book}
db_response_strict = {"type": "array", "items": {**db_book, "additionalProperties": False}}
basic = {"type": "object", "required": ["title"], "properties": {
    "title": {"type": "string"}, "publishers": strings, "number_of_pages": {"type": "integer"}, "weight": {"type": "string"},
    "physical_format": {"type": "string"}, "subjects": strings, "isbn_13": strings, "isbn_10": strings,
    "publish_date": {"type": "string"}, "physical_dimensions": {"type": "string"}}}
isbn13, isbn10 = {"type": "object", "required": ["isbn_13"]}, {"type": "object", "required": ["isbn_10"]}
book_info = {"allOf": [basic, {"anyOf": [isbn13, isbn10]}]}
book_info_one = {"allOf": [basic, {"oneOf": [isbn13, isbn10]}]}

print("Search requests (listings 7.6-7.9)")
request = {"title": "habit", "fields": ["title", "weight", "number_of_pages"]}
report("7.8  title, fields of strings", search_request, request)
report("7.9  'tilte' typo", search_request, {"tilte": "habit", "fields": request["fields"]})
report("7.7  the same request against the enum of 7.6", search_request_enum, request)
print()
print("Database responses (listings 7.13-7.15)")
rows = [{"title": "7 Habits of Highly Effective People", "available": True, "isbn": "978-0812981605", "dummy_property": 42},
        {"title": "The Power of Habit", "available": False, "isbn": "978-1982137274", "dummy_property": 45}]
report("7.14 extra dummy_property, default schema", db_response, rows)
report("7.15 extra dummy_property, additionalProperties: false", db_response_strict, rows)
print()
print("Open Library responses (listings 7.16-7.19)")
watchmen = {"publishers": ["DC Comics"], "number_of_pages": 334, "weight": "1.4 pounds", "physical_format": "Paperback",
            "subjects": ["Graphic Novels", "Comics & Graphic Novels", "Fiction", "Fantastic fiction"],
            "isbn_13": ["9780930289232"], "title": "Watchmen", "isbn_10": ["0930289234"], "publish_date": "April 1, 1995",
            "physical_dimensions": "10.1 x 6.6 x 0.8 inches"}
no_isbn = {k: x for k, x in watchmen.items() if not k.startswith("isbn")}
only10 = {k: x for k, x in watchmen.items() if k != "isbn_13"}
report("7.19 Watchmen (both ISBNs), allOf + anyOf", book_info, watchmen)
report("     Watchmen with only isbn_10, allOf + anyOf", book_info, only10)
report("     Watchmen with no ISBN, allOf + anyOf", book_info, no_isbn)
report("     Watchmen (both ISBNs), allOf + oneOf", book_info_one, watchmen)
print()
print("Error details (listings 7.20-7.23)")
bad = {"myTitle": "habit", "fields": [1, 2]}
print("7.21 first error only:", json.dumps(validate(search_request, {"myTitle": "habit", "fields": request["fields"]})))
report("7.23 myTitle and fields [1, 2], first error (default)", search_request, bad)
report("7.23 myTitle and fields [1, 2], allErrors: true", search_request, bad, all_errors=True)
