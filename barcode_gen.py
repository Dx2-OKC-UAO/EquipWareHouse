# В этом примере кода показано, как создать штрих-код Code 39 Standard.
import aspose.barcode as barcode
import os
from PIL import Image

# Инициализировать генератор штрих-кода
# Укажите тип кодирования
generator = barcode.generation.BarcodeGenerator(barcode.generation.EncodeTypes.CODE_39_STANDARD)

# Текст кода
generator.code_text = "1234567890"

# Сохраните сгенерированный штрих-код
generator.save("Code39Standard.jpg")
#os.startfile("Code39Standard.jpg", "print")
myImage=Image.open("Code39Standard.jpg")
myImage.show()