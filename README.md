# uncompressed-png
Simple python script to convert RGB and RGBA into uncompressed format and back

## Requirements
 - Python
 - `numpy`, `python-opencv`, `tqdm` modules

## .upng format
Header format:
| Byte index | Size in bytes | Type         | Name      | Dscription            |
|------------|---------------|--------------|-----------|-----------------------|
| 0          | 4             | ASCII string | prefix    | Always "UPNG"         |
| 4          | 4             | uint32       | height    | Height of image       |
| 8          | 4             | uint32       | width     | Width of image        |
| 9          | 1             | byte         | channels  | Channels count        |
| 10         | 1             | byte         | separator | Always 0x0            |

All next bytes is colour values, 3 or 4 unsgined bytes color values in RGB or RGBA format without any separator
