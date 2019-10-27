# Collection of registers and their bit fields

## Motivation:
Writing all registers and bit fields by hand it error prone and tideus.
While generating c++ header files with registers and bit fields,
I've noticed seriuos bugs and Inconsistencies in atdf files (see below).
Microchip is not responding to any mail reporting this issue.
That is why this repository exists.

You can find them in `registers` directory in `yaml` format for easy parsing and reading.
Original files can be downloaded from [here](http://packs.download.atmel.com/).

### Known bugs in original files:
* missing bit fields
* wrongly named bit fields
* missing registers
* `Res`, `Reserved` bit fields which should not exist

### Inconsistencies in original files:
* Same attribute names are represented in hex as well in int.

For all fixes see git log for atdf files.
