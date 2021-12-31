from PIL import Image
I = Image.open('hh.JPG')
I.show()
L = I.convert('L')
L.show()