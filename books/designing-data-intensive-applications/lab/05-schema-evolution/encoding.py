"""Schema-driven binary encodings and their compatibility rules.

Reproduces the sizes of the book's example record (Example 5-2) in JSON,
a Protocol Buffers-style tag/wire-type encoding, and an Avro-style
schema-resolved encoding — then shows forward and backward compatibility.

Illustrates DDIA 2nd ed., Chapter 5, "Protocol Buffers" and "Avro"
(pp. 169-177). The encoders are the vault's own, minimal implementations of
the wire formats as the book describes them.
"""

from __future__ import annotations

import json

RECORD = {"userName": "Martin", "favoriteNumber": 1337, "interests": ["daydreaming", "hacking"]}

# ---------------------------------------------------------------- varints

def varint(n: int) -> bytes:
    out = bytearray()
    while True:
        byte = n & 0x7F
        n >>= 7
        if n:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def read_varint(buf: bytes, i: int) -> tuple[int, int]:
    shift = result = 0
    while True:
        b = buf[i]
        i += 1
        result |= (b & 0x7F) << shift
        if not b & 0x80:
            return result, i
        shift += 7


def zigzag(n: int) -> int:
    return (n << 1) ^ (n >> 63)


def unzigzag(n: int) -> int:
    return (n >> 1) ^ -(n & 1)

# ------------------------------------------------- Protocol Buffers style
# Each field: varint(tag << 3 | wire_type) then the value.
# wire type 0 = varint, 2 = length-delimited (strings; repeated fields repeat the tag).

PB_V1 = {"userName": (1, "string"), "favoriteNumber": (2, "int"), "interests": (3, "repeated string")}
PB_V2 = {**PB_V1, "email": (4, "string")}            # v2 adds an optional field with a new tag


def pb_encode(record: dict, schema: dict) -> bytes:
    out = bytearray()
    for name, (tag, typ) in schema.items():
        if name not in record:
            continue                                  # absent optional field: simply not encoded
        values = record[name] if typ.startswith("repeated") else [record[name]]
        for v in values:
            if typ == "int":
                out += varint(tag << 3 | 0) + varint(v)
            else:
                data = v.encode()
                out += varint(tag << 3 | 2) + varint(len(data)) + data
    return bytes(out)


def pb_decode(buf: bytes, schema: dict) -> tuple[dict, list[int]]:
    by_tag = {tag: (name, typ) for name, (tag, typ) in schema.items()}
    record: dict = {}
    skipped: list[int] = []
    i = 0
    while i < len(buf):
        key, i = read_varint(buf, i)
        tag, wire = key >> 3, key & 7
        if wire == 0:
            value, i = read_varint(buf, i)
        else:
            length, i = read_varint(buf, i)
            value, i = buf[i:i + length].decode(), i + length
        if tag not in by_tag:                         # unknown tag: the wire type tells us how far to skip
            skipped.append(tag)
            continue
        name, typ = by_tag[tag]
        if typ.startswith("repeated"):
            record.setdefault(name, []).append(value)
        else:
            record[name] = value
    return record, skipped

# ------------------------------------------------------------ Avro style
# No tags: fields are encoded in schema order. Reader and writer schemas are
# resolved by field *name*; missing fields take the reader's default.

AVRO_V1 = [("userName", "string", None), ("favoriteNumber", "union[null,long]", None),
           ("interests", "array<string>", None)]
AVRO_V2 = AVRO_V1 + [("email", "union[null,string]", ("default", None))]


def avro_encode(record: dict, schema: list) -> bytes:
    out = bytearray()
    for name, typ, _ in schema:
        v = record.get(name)
        if typ == "string":
            data = v.encode()
            out += varint(zigzag(len(data))) + data
        elif typ.startswith("union"):
            if v is None:
                out += varint(zigzag(0))              # branch 0 = null
            elif "long" in typ:
                out += varint(zigzag(1)) + varint(zigzag(v))
            else:
                data = v.encode()
                out += varint(zigzag(1)) + varint(zigzag(len(data))) + data
        elif typ == "array<string>":
            out += varint(zigzag(len(v)))
            for s in v:
                data = s.encode()
                out += varint(zigzag(len(data))) + data
            out += varint(0)                          # end of array blocks
    return bytes(out)


def avro_decode(buf: bytes, writer: list, reader: list) -> dict:
    i, decoded = 0, {}
    for name, typ, _ in writer:                       # bytes can only be parsed with the writer's schema
        if typ == "string":
            n, i = read_varint(buf, i)
            n = unzigzag(n)
            decoded[name], i = buf[i:i + n].decode(), i + n
        elif typ.startswith("union"):
            branch, i = read_varint(buf, i)
            if unzigzag(branch) == 0:
                decoded[name] = None
            elif "long" in typ:
                v, i = read_varint(buf, i)
                decoded[name] = unzigzag(v)
            else:
                n, i = read_varint(buf, i)
                n = unzigzag(n)
                decoded[name], i = buf[i:i + n].decode(), i + n
        elif typ == "array<string>":
            count, i = read_varint(buf, i)
            items = []
            for _ in range(unzigzag(count)):
                n, i = read_varint(buf, i)
                n = unzigzag(n)
                items.append(buf[i:i + n].decode())
                i += n
            _, i = read_varint(buf, i)
            decoded[name] = items
    result = {}
    for name, _, default in reader:                   # schema resolution by field name
        if name in decoded:
            result[name] = decoded[name]
        elif default is not None:
            result[name] = default[1]
        else:
            raise ValueError(f"reader requires field {name!r} with no default")
    return result                                     # fields only the writer knows are ignored


def main() -> None:
    js = json.dumps(RECORD, separators=(",", ":")).encode()
    pb = pb_encode(RECORD, PB_V1)
    av = avro_encode(RECORD, AVRO_V1)
    print("Encoded size of the book's example record (Example 5-2):")
    print(f"  JSON (no whitespace)       {len(js):3d} bytes")
    print(f"  Protocol Buffers style     {len(pb):3d} bytes   {pb.hex(' ')}")
    print(f"  Avro style                 {len(av):3d} bytes   {av.hex(' ')}")

    print("\nProtocol Buffers: compatibility through tag numbers")
    new = dict(RECORD, email="martin@example.com")
    old_view, skipped = pb_decode(pb_encode(new, PB_V2), PB_V1)
    print(f"  forward  (v1 reader, v2 data): skipped unknown tag(s) {skipped}; read {old_view}")
    new_view, _ = pb_decode(pb, PB_V2)
    print(f"  backward (v2 reader, v1 data): email absent -> {new_view.get('email', '<default>')!r}")

    print("\nAvro: compatibility through writer/reader schema resolution")
    print(f"  backward (v2 reader, v1 data): {avro_decode(av, AVRO_V1, AVRO_V2)}")
    print(f"  forward  (v1 reader, v2 data): {avro_decode(avro_encode(new, AVRO_V2), AVRO_V2, AVRO_V1)}")
    bad_reader = AVRO_V1 + [("email", "union[null,string]", None)]
    try:
        avro_decode(av, AVRO_V1, bad_reader)
    except ValueError as e:
        print(f"  adding a field WITHOUT a default breaks backward compatibility: {e}")


if __name__ == "__main__":
    main()
