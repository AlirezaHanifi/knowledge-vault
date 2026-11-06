# A mini JSON Schema validator

The chapter's JSON Schema keywords in about a hundred lines of Python: `type`, `properties`, `required`, `items`, `enum`, `additionalProperties`, `allOf`, `anyOf` and `oneOf`. Errors come in Ajv's style, with an all-errors switch. The script runs the chapter's requests, database responses and Open Library responses through it.

*Illustrates Data-Oriented Programming, chapter 7, pp. 144–161 (listings 7.6–7.23). The validator is the vault's; it is a teaching subset, not a full JSON Schema implementation.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 mini_json_schema.py
```

## Expected output

```text
Search requests (listings 7.6-7.9)
7.8  title, fields of strings                              valid
7.9  'tilte' typo                                          INVALID: data must have required property 'title'
7.7  the same request against the enum of 7.6              INVALID: data/fields/0 must be equal to one of the allowed values

Database responses (listings 7.13-7.15)
7.14 extra dummy_property, default schema                  valid
7.15 extra dummy_property, additionalProperties: false     INVALID: data/0 must NOT have additional properties

Open Library responses (listings 7.16-7.19)
7.19 Watchmen (both ISBNs), allOf + anyOf                  valid
     Watchmen with only isbn_10, allOf + anyOf             valid
     Watchmen with no ISBN, allOf + anyOf                  INVALID: data must match a schema in anyOf
     Watchmen (both ISBNs), allOf + oneOf                  INVALID: data must match exactly one schema in oneOf

Error details (listings 7.20-7.23)
7.21 first error only: [{"instancePath": "", "schemaPath": "#/required", "keyword": "required", "message": "must have required property 'title'"}]
7.23 myTitle and fields [1, 2], first error (default)      INVALID: data must have required property 'title'
7.23 myTitle and fields [1, 2], allErrors: true            INVALID: data must have required property 'title', data/fields/0 must be string, data/fields/1 must be string
```

## What to look for

- The request of listings 7.7–7.8 asks for a `title` field, which the enum of listing 7.6 doesn't list. Against that schema it is invalid.
- Unspecified fields are allowed by default (`dummy_property` passes) until `additionalProperties: false`.
- `allOf` with `anyOf` accepts Watchmen with both ISBNs or only one, and rejects it with none. With `oneOf` instead of `anyOf`, Watchmen fails, because it has both.
- By default only the first failure is reported. With all errors on, listing 7.23's request yields the three errors the book shows.

## Related

- Chapter note: [7. Basic data validation](../../chapters/07-basic-data-validation.md) — sections 7.2–7.5, pp. 144–161
