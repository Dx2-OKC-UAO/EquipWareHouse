# В этом примере кода показано, как создать штрих-код Code 39 Standard.
import aspose.barcode as barcode
import os
from PIL import Image

def generate_barcode(bar):

# Инициализировать генератор штрих-кода
# Укажите тип кодирования
    generator = barcode.generation.BarcodeGenerator(barcode.generation.EncodeTypes.CODE_39_STANDARD)
    generator.code_text = "45149581483"
    generator.save("Code39Standard.jpg")
    myImage=Image.open("Code39Standard.jpg")
    myImage.show()