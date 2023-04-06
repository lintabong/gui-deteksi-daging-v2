import sys
import os
import tkinter
import ctypes
import cv2
import threading
import pywt
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from skimage.feature import graycomatrix

sys.path.insert(1, os.path.abspath(os.path.join(os.getcwd())))
import predict


ctypes.windll.shcore.SetProcessDpiAwareness(1)

filepath = ""

def process_image():
    global filepath

    img     = cv2.imread(filepath)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue     = img_hsv[:,:,0].mean()

    saturation = img_hsv[:, :, 1].mean()
    glcm       = graycomatrix(img[:, :, 1], 
                              distances=[5], 
                              angles=[0], 
                              levels=256,
                              symmetric=True, 
                              normed=True).mean()

    r = 0
    g = 0
    b = 0

    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if img[i][j][0] >= 125:
                r += 1
            if img[i][j][1] >= 125:
                g += 1
            if img[i][j][2] >= 125:
                b += 1
        
    in_red.insert(0, r)
    in_green.insert(0, g)
    in_blue.insert(0, b)
    in_glcm.insert(0, glcm)
    in_hue.insert(0, hue)
    in_saturation.insert(0, saturation)

    result = predict.run(filepath)

    in_result.insert(2, result)


def load_image(size=350, xd=40, yd=40):
    global filepath

    fileToRead = ["*.png", "*.jpeg", "*jpg"]

    file = tkinter.filedialog.askopenfile(
        mode = "r", 
        filetypes = [("Image file", fileToRead)]
    )

    if file:
        filepath = os.path.abspath(file.name)
        
        image1 = Image.open(filepath)
        image1 = image1.resize((size, size))
        image1 = ImageTk.PhotoImage(image1)

        label1 = tkinter.Label(image=image1)
        label1.image = image1

        label1.place(x=xd, y=yd)

        fullname   = os.path.basename(filepath).split("\\")[-1]
        filename   = fullname.split(".")[0]
        fileformat = fullname.split(".")[-1]
        filesize   = os.stat(filepath).st_size

        in_filename.insert(2, filename)
        in_filesize.insert(2, filesize)
        in_format.insert(2, fileformat)

        fig  = Figure(figsize = (2.5, 2.5), dpi = 100)
        img  = cv2.imread(filepath)
        vals = img.mean(axis=2).flatten()
        a = fig.add_subplot(111)
        a.hist(vals, 255)
        canvas = FigureCanvasTkAgg(fig,  master = frame_histogram)  
        canvas.draw()
        canvas.get_tk_widget().place(x=20, y=20)

        threading.Thread(target=process_image).start()


root = tkinter.Tk()

w = 1220
h = 830

root.geometry(f'{w}x{h}')
root.title("GUI Deteksi Daging")
root.option_add("*Font", 30)
root.resizable(False, False)
root.overrideredirect(False)

but_load_image = tkinter.Button(root, text = "Load Image", width = 12, command = lambda : load_image())
but_load_image.place(x = 40, y = 420)

but_save_data = tkinter.Button(root, text = "Save Data", width = 12)
but_save_data.place(x = 250, y = 420)

# RESULT FRAME
frame_result = tkinter.Frame(root, bg="#afa013", width=740, height=120)
frame_result.place(x=430, y=410)

text_result = tkinter.Label(frame_result, bg="#afa013", fg="#ffffff", text="hasil")
text_result.place(x=10, y=43)

in_result = tkinter.Entry(frame_result, width=20)
in_result.place(x=100, y=43)

# TABLE FRAME
frame_table = tkinter.Frame(root, bg="#5C6592", width=740, height=250)
frame_table.place(x=430, y=550)

for i in range(25, 235, 35):
    tkinter.Frame(frame_table, height=25, width=50, background='white').place(x=25, y=i)
    tkinter.Frame(frame_table, height=25, width=120, background='white').place(x=85, y=i)
    tkinter.Frame(frame_table, height=25, width=120, background='white').place(x=215, y=i)

# PARAMETER FRAME
frame_parameter = tkinter.Frame(root, bg="#afa013", width=350, height=350)
frame_parameter.place(x=430, y=40)

text_red = tkinter.Label(frame_parameter, bg="#afa013", fg="#ffffff", text="Red")
text_red.place(x=10, y=10)

text_green = tkinter.Label(frame_parameter, bg="#afa013", fg="#ffffff", text="Green")
text_green.place(x=10, y=60)

text_blue = tkinter.Label(frame_parameter, bg="#afa013", fg="#ffffff", text="Blue")
text_blue.place(x=10, y=110)

text_glcm = tkinter.Label(frame_parameter, bg="#afa013", fg="#ffffff", text="GLCM")
text_glcm.place(x=10, y=160)

text_hue = tkinter.Label(frame_parameter, bg="#afa013", fg="#ffffff", text="Hue")
text_hue.place(x=10, y=210)

text_saturation = tkinter.Label(frame_parameter, bg="#afa013", fg="#ffffff", text="Saturation")
text_saturation.place(x=10, y=260)

text_value = tkinter.Label(frame_parameter, bg="#afa013", fg="#ffffff", text="Value")
text_value.place(x=10, y=310)

in_red = tkinter.Entry(frame_parameter, width=20)
in_red.place(x=100, y=13)

in_green = tkinter.Entry(frame_parameter, width=20)
in_green.place(x=100, y=63)

in_blue = tkinter.Entry(frame_parameter, width=20)
in_blue.place(x=100, y=113)

in_glcm = tkinter.Entry(frame_parameter, width=20)
in_glcm.place(x=100, y=163)

in_hue = tkinter.Entry(frame_parameter, width=20)
in_hue.place(x=100, y=213)

in_saturation = tkinter.Entry(frame_parameter, width=18)
in_saturation.place(x=120, y=263)

in_value = tkinter.Entry(frame_parameter, width=18)
in_value.place(x=120, y=313)

# HISTOGRAM FRAME
frame_histogram = tkinter.Frame(root, bg="#afa013", width=350, height=350)
frame_histogram.place(x=820, y=40)

# INFORMATION FRAME
frame_information = tkinter.Frame(root, bg="#afa013", width=350, height=170)
frame_information.place(x=40, y=490)

text_filename = tkinter.Label(frame_information, bg="#afa013", fg="#ffffff", text="filename")
text_filename.place(x=10, y=10)

text_filesize = tkinter.Label(frame_information, bg="#afa013", fg="#ffffff", text="filesize")
text_filesize.place(x=10, y=60)

text_format = tkinter.Label(frame_information, bg="#afa013", fg="#ffffff", text="format")
text_format.place(x=10, y=110)

in_filename = tkinter.Entry(frame_information, width=20)
in_filename.place(x=100, y=13)

in_filesize = tkinter.Entry(frame_information, width=20)
in_filesize.place(x=100, y=63)

in_format = tkinter.Entry(frame_information, width=20)
in_format.place(x=100, y=113)

# IMAGE
sizeImg = 350
image = Image.open("insertimg.png")
image = image.resize((sizeImg, sizeImg))
image = ImageTk.PhotoImage(image)

image1 = tkinter.Label(image=image)
image1.image = image
image1.place(x=40, y=40)


root.mainloop()
