import cv2
import numpy as np
from tqdm import tqdm
from io import BufferedWriter, BufferedReader
import sys

H_EXT = "UPNG"
ZERO = bytes((0x00, ))

def create_bar(name: str, max: int):
    return tqdm(total=max, ncols=100, bar_format='{desc} |{bar}| {n_fmt}/{total_fmt}; ETA: {remaining}; {elapsed}', desc=name)

def _write_header(file: BufferedWriter, size: tuple[int, int], channels: int):
    file.write(H_EXT.encode("ascii"))
    file.write(size[0].to_bytes(4, "little"))
    file.write(size[1].to_bytes(4, "little"))
    file.write(channels.to_bytes(1, "little"))
    file.write(ZERO)

def _read_header(file: BufferedReader) -> tuple[int, int, int]:
    type = file.read(4).decode("ascii")
    if type != H_EXT:
         raise ValueError("Uncorrect file type")
    h = int.from_bytes(file.read(4), 'little')
    w = int.from_bytes(file.read(4), 'little')
    ch = int.from_bytes(file.read(1), 'little')
    if file.read(1)[0] != 0:
        raise ValueError("Invalid header")
    return (h, w, ch)

def _read_col(file: BufferedReader, channels: int) -> np.ndarray[np.uint8]:
    if channels == 4:
        r = int.from_bytes(file.read(1), 'little')
        g = int.from_bytes(file.read(1), 'little')
        b = int.from_bytes(file.read(1), 'little')
        a = int.from_bytes(file.read(1), 'little')
        return np.array([b, g, r, a], dtype=np.uint8) # bgra
    elif channels == 3:
        r = int.from_bytes(file.read(1), 'little')
        g = int.from_bytes(file.read(1), 'little')
        b = int.from_bytes(file.read(1), 'little')
        return np.array([b, g, r], dtype=np.uint8) # bgr
    else:
        raise ValueError("Only 3 and 4 channels supported")

def _write_col(file: BufferedWriter, values: list[int]):
    for v in values:
         file.write(v.to_bytes(1, "little"))

def uncompress(image_path: str, output="out.upng", log=False):
    image: np.ndarray[np.ndarray[int]] = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        if log:
            print("Failed to load the image.")
        return
    
    height, width, channels = image.shape
    out = open(output, "wb")
    _write_header(out, (height, width), channels)
    if log:
        bar = create_bar(f"Uncompressing {width}x{height}, {channels}", height*width)
    for y in range(height):
            for x in range(width):
                pixel: np.ndarray[np.uint8] = image[y, x]
                blue = int(pixel[0])
                green = int(pixel[1])
                red = int(pixel[2])
                if channels == 4:
                    alpha = int(pixel[3])
                    _write_col(out, [red, green, blue, alpha])
                else:
                    _write_col(out, [red, green, blue])
                if log:
                    bar.update()
    out.close()

def compress(image_path: str, output="out.png", log=False):
    inp = open(image_path, "rb")
    h, w, ch = _read_header(inp)
    if log:
        bar = create_bar(f"Compressing {w}x{h}, {ch}", h*w)
    out = np.zeros((h, w, ch), np.uint8)
    for row in range(h):
        for col in range(w):
            values = _read_col(inp, ch)
            out[row, col] = values
            if log:
                bar.update()
    cv2.imwrite(output, out)

if __name__ == "__main__":
    uncompress(sys.argv[1], log=True)
    compress("out.upng", log=True)