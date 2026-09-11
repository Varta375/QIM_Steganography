[English](README.md) | [Russian](README.ru.md)

# Quantization Index Modulation (QIM) steganography method

Программа для сокрытия информации в изображении. Метод заключается в изменении значений пикселей изображения в зависимости от значений встроенных битов сообщения. Эта реализация является пространственной версией (т.е. встраивание происходит в пиксели), поэтому любое искажение (изменение яркости/резкости/контраста и т.д.) почти гарантированно уничтожит встроенную информацию, но это зависит от используемого изображения и шага квантования (q).

Шаг квантования в нашем случае отвечает за робастность изображения и заметность сообщения: чем больше вы попробуете его сделать, тем больше вероятность того, что сообщение переживет незначительную атаку, но при этом увеличится заметность артефактов изображения. 


## Достойно внимания

Программа автоматически конвертирует другие форматы изображений в PNG, так как это не формат с потерями, и закодированная информация не будет уничтожена сразу после завершения программы. Также не забывайте указывать путь стегоизображения, когда используете аргумент чтения.

## Установка

Склонируйте репозиторий и скачайте зависимости из requirements.txt

```bash
pip install -r requirements.txt
```
## Использование/Примеры

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
