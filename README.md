# uncompressed-png
Simple python script to convert RGB and RGBA into uncompressed format and back

## Requirements
 - Python
 - `numpy`, `python-opencv`, `tqdm` modules

## .upng format
Header format:
| Byte index | Size in bytes | Name      | Dscription            |
|------------|---------------|-----------|-----------------------|
| 0          | 4             | prefix    | Always UPNG, in ascii |
| 4          | 4             | height    | Height of image       |
| 8          | 4             | width     | Width of image        |
| 9          | 1             | channels  | Channels count        |
| 10         | 1             | separator | Always 0x0            |

All next bytes is colours, 3 or 4 unsgined bytes color values in RGB or RGBA format without any separator
