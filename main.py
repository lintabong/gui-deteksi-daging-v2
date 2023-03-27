import os
import tkinter
import ctypes
from tkinter.filedialog import askopenfile
from PIL import ImageTk, Image

ctypes.windll.shcore.SetProcessDpiAwareness(1)


def load_image(root, size, xd, yd):

   fileToRead = ['*.png','*.jpeg','*jpg']

   file = askopenfile(mode = 'r', filetypes = [('Image file', fileToRead)])

   if file:

      filepath = os.path.abspath(file.name)
      # filename = os.path.basename(filepath).split('\\')[-1]

      image1 = Image.open(filepath)
      image1 = image1.resize((size, size))

      image1 = ImageTk.PhotoImage(image1)

      label1 = tkinter.Label(image=image1)
      label1.image = image1

      label1.place(x=xd, y=yd)

      printpath = tkinter.Label(root, text=filepath)
      printpath.place(x=250, y=696)


def load_model():

   global model_filepath

   fileToRead = ['*.jpeg']

   file = askopenfile(mode = 'r', filetypes = [('Model file', fileToRead)])

   if file:

      filepath = os.path.abspath(file.name)

      model_filepath = filepath


def predict_image():

   global model_filepath

   print(model_filepath)

root = tkinter.Tk()

w = 1250
h = 830

root.geometry(str(w) + 'x' + str(h))
root.title('GUI Deteksi Keretakan Lapisan')
root.option_add('*Font', 30)
root.resizable(False, False)
root.overrideredirect(False)

entryFilepath = tkinter.Entry(root, width=70)
entryFilepath.place(x=150, y=636)

butLoadModel = tkinter.Button(root, text = 'Load Model', width = 15, command = lambda : function.load_model())
butLoadModel.place(x = 60, y = 630)

butLoadImage = tkinter.Button(root, text = 'Load Image', width = 15, command = lambda : function.load_image(root, 450, 150, 100))
butLoadImage.place(x = 60, y = 690)

butDetectImage = tkinter.Button(root, text = 'Detect', width = 15, command = lambda : function.predict_image())
butDetectImage.place(x = 60, y = 750)

sizeImg = 450
image = Image.open('insertimg.png')
image = image.resize((sizeImg, sizeImg))
image = ImageTk.PhotoImage(image)

image1 = tkinter.Label(image=image)
image1.image = image
image1.place(x=150, y=100)

# image right initiation and positioning
image2 = tkinter.Label(image=image)
image2.image = image
image2.place(x=650, y=100)

root.mainloop()