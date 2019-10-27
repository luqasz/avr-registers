# Fixed version of `atdf` and `pic` files for atmega.

Known bugs:
* Missing `WGM` bit fields. e.g. `WGM11` should exist, instead WGM1 with a mask field set to non power of two.
* Bit fields named `Res` or `Reserved`, which indicates that they are reserved. They should not exist in file.
* Missing bit fields in `TWAR1` for `atmega328pb`.

Inconsistencies:
* Same attribute names are represented in hex as well in int.

For all fixes see git log for atdf files.
