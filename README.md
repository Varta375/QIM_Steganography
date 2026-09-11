[English](README.en.md) | [Russian](README.ru.md)

# Quantization Index Modulation (QIM) steganography method

A program for hiding information in an image. The method consists of changing the pixel values of the image depending on the values of the embedded bits of the message. This implementation is a spatial version (i.e. embedding occurs in pixels), so any distortion (changing brightness/sharpness/contrast, etc.) is almost guaranteed to destroy the embedded information, but this depends on the image used and the quantization step (q). The quantization step in our case is responsible for the robustness of the image and the visibility of the message: the more you try to make it, the more likely it is that the message will survive a minor attack, but it will increase the visibility of the image artifacts.

The quantization step in our case is responsible for the robustness of the image and the visibility of the message: the more you try to make it, the more likely it is that the message will survive a minor attack, but at the same time the visibility of the image artifacts will increase.

## Honorable Mention

The program automatically converts other image formats to PNG because it is not a lossy format, and the encoded information will not be destroyed immediately after the program is terminated.

Also do not forget to put stegoimage path when you use reading argument.
## Installation
Clone the repository and download dependencies from requirements.txt

```bash
pip install -r requirements.txt
```


    
## Usage/Examples

```python
QIM_Method.py

Usage:
    QIM_Method.py [-h] write -t <text_input> -i <image_input> [-q <quantization_step>]
    QIM_Method.py [-h] read -i <image_input> [-q <quantization_step>] -l <message_length>

Options:
    -h, --help                      Show options
    -t, --text=<text_input>         Text input
    -i, --in=<image_input>          Image path of steganography container
    -q, --quantization=<step>       Quantization step [default: 4]
    -l, --length=<message_length>   Length of encoded message
    -v, --version                   Show the version

    QIM_Method.py write -t "Hello world!" -i image.png -q 8
    Output path: image_qim.png
    Message length: 12 
    Quantization step: 8

    QIM_Method.py read -i image_qim.png -q 8 -l 12
    Decoded message: Hello world!
```
