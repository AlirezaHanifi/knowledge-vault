# Binary encodings and schema evolution

Minimal encoders for the Protocol Buffers wire format (field tags + wire types + varints) and the Avro binary format (no tags; zigzag varints; reader/writer schema resolution). Encodes the book’s example record (Example 5-2) and reproduces the sizes the book reports — 81 bytes of JSON, 33 bytes of Protocol Buffers, 32 bytes of Avro — then demonstrates forward and backward compatibility.

*Illustrates DDIA 2nd ed., “Protocol Buffers” and “Avro”, pp. 169–177. The implementation is the vault’s own.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 encoding.py
```

## Expected output

```text
Encoded size of the book's example record (Example 5-2):
  JSON (no whitespace)        81 bytes
  Protocol Buffers style      33 bytes   0a 06 4d 61 72 74 69 6e 10 b9 0a 1a 0b 64 61 79 64 72 65 61 6d 69 6e 67 1a 07 68 61 63 6b 69 6e 67
  Avro style                  32 bytes   0c 4d 61 72 74 69 6e 02 f2 14 04 16 64 61 79 64 72 65 61 6d 69 6e 67 0e 68 61 63 6b 69 6e 67 00

Protocol Buffers: compatibility through tag numbers
  forward  (v1 reader, v2 data): skipped unknown tag(s) [4]; read {'userName': 'Martin', 'favoriteNumber': 1337, 'interests': ['daydreaming', 'hacking']}
  backward (v2 reader, v1 data): email absent -> '<default>'

Avro: compatibility through writer/reader schema resolution
  backward (v2 reader, v1 data): {'userName': 'Martin', 'favoriteNumber': 1337, 'interests': ['daydreaming', 'hacking'], 'email': None}
  forward  (v1 reader, v2 data): {'userName': 'Martin', 'favoriteNumber': 1337, 'interests': ['daydreaming', 'hacking']}
  adding a field WITHOUT a default breaks backward compatibility: reader requires field 'email' with no default
```

## What to look for

- Byte-for-byte: `0a 06 4d 61 72 74 69 6e` is tag 1, wire type 2, length 6, “Martin”.
- Protocol Buffers achieves forward compatibility because an old reader can skip an unknown tag — the wire type says how many bytes to skip.
- Avro has no tags at all; compatibility comes from resolving the writer’s schema against the reader’s by field name, which is why an added field needs a default.

## Related

- Chapter note: [5. Encoding and Evolution](../../chapters/05-encoding-and-evolution.md) — “Protocol Buffers” and “Avro”, pp. 169–177
