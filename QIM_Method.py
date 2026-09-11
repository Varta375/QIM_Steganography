"""
QIM_Method.py

Usage:
    QIM_Method.py [-h] write -t <text_input> -i <image_input> [-q <quantization_step>]
    QIM_Method.py [-h] read -i <stegoimage_input> [-q <quantization_step>] -l <message_length>

Options:
    -h, --help                      Show options
    -t, --text=<text_input>         Text input
    -i, --in=<image_input>          Image path of steganography container
    -q, --quantization=<step>       Quantization step [default: 4]
    -l, --length=<message_length>   Length of encoded message
    -v, --version                   Show the version
"""

from PIL import Image
import numpy as np
import math
from docopt import docopt

class QIMException(Exception):
    pass

class QIM():
    def __init__(self, image_path):
        self.image = Image.open(image_path).convert("RGB")
        image_array = np.array(self.image)
        self.height, self.width, self.channels = image_array.shape

    @staticmethod
    def message_to_bits(message: str) -> list[int]:
        data = message.encode("utf-8")
        bits = []

        for byte in data:
            for shift in range(7, -1, -1):
                bits.append((byte >> shift) & 1)

        return bits

    @staticmethod
    def bits_to_message(bits) -> str:
        if len(bits) % 8 != 0:
            raise ValueError("The number of bits must be a multiple of 8")

        data = bytearray()
        for i in range(0, len(bits), 8):
            byte = 0
            for bit in bits[i:i + 8]:
                bit = int(bit)
                if bit not in (0, 1):
                    raise ValueError(f"Invalid bit value: {bit}")
                byte = (byte << 1) | bit

            data.append(byte)
        return data.decode("utf-8")

    @staticmethod
    def embed_pixel(p_i, m_i, q) -> int:
        return int((q * math.floor(p_i / q)) + (q//2) * m_i)

    @staticmethod
    def bit_extract(p_ii, q) -> str:
        p_ii = int(p_ii)
        p_0 = q * math.floor(p_ii / q) + 0
        p_1 = q * math.floor(p_ii / q) + (q // 2)
        if abs(p_ii - p_0) < abs(p_ii - p_1):
            return "0"
        else:
            return "1"

    def write(self, image_path, message,q):
        img = Image.open(image_path).convert("RGB")
        pixel_array = np.array(img)
        image_shape = pixel_array.shape
        pixel_list = pixel_array.flatten().astype(float)
        bits = self.message_to_bits(message)

        for i in range(len(bits)):
            pixel_list[i] = self.embed_pixel(pixel_list[i], bits[i], q)

        edited_array = pixel_list.reshape(image_shape).clip(0, 255).astype(np.uint8)
        edited_image = Image.fromarray(edited_array)
        output_path = image_path.rsplit('.', 1)[0] + "_qim.png"
        edited_image.save(output_path, format = "PNG")

        return output_path

    def read(self, stegoimage_path, message_length, q=4):
        img = Image.open(stegoimage_path).convert("RGB")
        pixel_array = np.array(img)
        pixel_list = pixel_array.flatten()
        bytes_total = message_length * 8

        if bytes_total > len(pixel_list):
            raise QIMException(f"Message is too large: need {bytes_total} bits")

        bits = []

        for i in range(bytes_total):
            bits.append(self.bit_extract(pixel_list[i], q))

        return self.bits_to_message(bits)


def main():
    args = docopt(__doc__ or "", version="qim 1.0")
    try:
        image_path = args["--in"]
        q = int(args["--quantization"])
        steg = QIM(image_path)

        if args["write"]:
            text = args["--text"]
            result = steg.write(image_path, text, q)
            print(f"Output path: {result} \nMessage length: {len(text.encode("utf-8"))} \nQuantization step: {q}")

        elif args["read"]:
            message_length = int(args["--length"])
            result = steg.read(image_path, message_length, q)
            print(f"Decoded message: {result}")


    except:
        raise QIMException("Use --help to see usage and options")

if __name__ == "__main__":
    main()