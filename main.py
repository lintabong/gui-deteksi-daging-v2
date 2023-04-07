import sys
import os
import tkinter
import ctypes
import cv2
import threading
from tkinter import END
from openpyxl import Workbook
from dotenv import load_dotenv
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sys.path.insert(1, os.path.abspath(os.path.join(os.getcwd())))
import functions.predict as predict
import functions.color as color
import functions.glcm as glcm
import functions.saturation as saturation
import functions.wvhar as wvhar

load_dotenv()
ctypes.windll.shcore.SetProcessDpiAwareness(1)


WIDTH          = int(os.getenv("WIDTH"))
HEIGHT         = int(os.getenv("HEIGHT"))
WHITE          = f'#{os.getenv("WHITE")}'
ORANGE         = f'#{os.getenv("ORANGE")}'
BLUE           = f'#{os.getenv("BLUE")}'
TITLE          = os.getenv("TITLE")
HISTOGRAM_SIZE = float(os.getenv("HISTOGRAM_SIZE"))


root = tkinter.Tk()
root.geometry(f'{WIDTH}x{HEIGHT}')
root.title(TITLE)
root.option_add("*Font", 30)
root.resizable(False, False)
root.overrideredirect(False)

filepath   = ""
data_excel = []
cursor     = 0


def process_image():
    global filepath

    r, g, b    = color.run(filepath)
    gray_level = glcm.run(filepath)
    hue, sat   = saturation.run(filepath)
    result     = predict.run(filepath)
    ori, mod   = wvhar.run(filepath)

    in_red.insert(2, r)
    in_green.insert(2, g)
    in_blue.insert(2, b)
    in_glcm.insert(2, gray_level)
    in_hue.insert(2, hue)
    in_saturation.insert(2, sat)
    in_result.insert(2, result)
    in_value.insert(2, ori)


def load_image(size=350, xd=40, yd=40):
    global filepath

    fileToRead = ["*.png", "*.jpeg", "*jpg"]

    file = tkinter.filedialog.askopenfile(
        mode = "r", 
        filetypes = [("Image file", fileToRead)]
    )

    in_red.delete(0, END)
    in_green.delete(0, END)
    in_blue.delete(0, END)
    in_glcm.delete(0, END)
    in_hue.delete(0, END)
    in_saturation.delete(0, END)
    in_value.delete(0, END)
    in_result.delete(0, END)
    in_filename.delete(0, END)
    in_filesize.delete(0, END)
    in_format.delete(0, END)

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

        fig  = Figure(figsize=(HISTOGRAM_SIZE, HISTOGRAM_SIZE), dpi=100)
        img  = cv2.imread(filepath)
        vals = img.mean(axis=2).flatten()
        a = fig.add_subplot(111)
        a.hist(vals, 255)
        canvas = FigureCanvasTkAgg(fig,  master = frame_histogram)  
        canvas.draw()
        canvas.get_tk_widget().place(x=20, y=20)

        threading.Thread(target=process_image).start()


def update_data():
    global data_excel
    global cursor
    global filepath

    ori, mod = wvhar.run(filepath)

    data = [len(data_excel)+1, ori, mod]

    data_excel.append(data)
    
    c = 0
    for i, dat in enumerate(data_excel):
        if len(data_excel) - i <= 4:
            tkinter.Label(frame_table, bg=WHITE, fg=ORANGE, text=dat[0]).place(x=41, y=(45*c)+75)
            tkinter.Label(frame_table, bg=WHITE, fg=ORANGE, text=dat[1]).place(x=151, y=(45*c)+75)
            tkinter.Label(frame_table, bg=WHITE, fg=ORANGE, text=dat[2]).place(x=401, y=(45*c)+75)
            c+=1

    cursor = len(data_excel)


def show_data():
    global data_excel

    for i in range(70, 235, 45):
        tkinter.Frame(frame_table, height=35, width=50, background=WHITE).place(x=25, y=i)
        tkinter.Frame(frame_table, height=35, width=215, background=WHITE).place(x=85, y=i)
        tkinter.Frame(frame_table, height=35, width=265, background=WHITE).place(x=310, y=i)

    c = 0
    for i, dat in enumerate(data_excel):
        if len(data_excel) - i <= 4 + (len(data_excel) - cursor):
            tkinter.Label(frame_table, bg=WHITE, fg=ORANGE, text=dat[0]).place(x=41, y=(45*c)+75)
            tkinter.Label(frame_table, bg=WHITE, fg=ORANGE, text=dat[1]).place(x=151, y=(45*c)+75)
            tkinter.Label(frame_table, bg=WHITE, fg=ORANGE, text=dat[2]).place(x=401, y=(45*c)+75)
            c+=1


def prev_data():
    global cursor

    if cursor >= 4:
        cursor-=1
        show_data()


def next_data():
    global cursor

    if cursor <= len(data_excel)-1:
        cursor+=1
        show_data()


def export_excel():
    global data_excel

    wb = Workbook()
    ws = wb.active

    for row in data_excel:
        ws.append(row)

    wb.save("result.xlsx")


but_load_image = tkinter.Button(root, text="Load Image", width=12, command=lambda:load_image())
but_save_data = tkinter.Button(root, text="Save Data", width=12, command=lambda:update_data())

# RESULT FRAME
frame_result = tkinter.Frame(root, bg=ORANGE, width=740, height=120)
frame_result.place(x=430, y=410)

text_result = tkinter.Label(frame_result, bg=ORANGE, fg=WHITE, text="Result")
text_result.place(x=10, y=43)

in_result = tkinter.Entry(frame_result, width=20)
in_result.place(x=100, y=43)

# TABLE FRAME
frame_table = tkinter.Frame(root, bg=BLUE, width=740, height=250)
frame_table.place(x=430, y=550)

for i in range(25, 235, 45):
    tkinter.Frame(frame_table, height=35, width=50, background=WHITE).place(x=25, y=i)
    tkinter.Frame(frame_table, height=35, width=215, background=WHITE).place(x=85, y=i)
    tkinter.Frame(frame_table, height=35, width=265, background=WHITE).place(x=310, y=i)

c = 0
xpos = [36, 100, 325]
for text in ["No", "WVHAR ORIGINAL", "WVHAR MODIFICATION"]:
    tkinter.Label(frame_table, bg=WHITE, fg=BLUE, text=text).place(x=xpos[c], y=28)
    c+=1

but_prev = tkinter.Button(frame_table, text="<<", width=4, command=lambda:prev_data())
but_next = tkinter.Button(frame_table, text=">>", width=4, command=lambda:next_data())
but_export = tkinter.Button(frame_table, text="Export Excel", width=12, command=lambda:export_excel())

# PARAMETER FRAME
frame_parameter = tkinter.Frame(root, bg=ORANGE, width=350, height=350)
frame_parameter.place(x=430, y=40)

c = 0
for text in ["Red", "Green", "Blue", "GLCM", "Hue", "Saturation", "Value"]:
    tkinter.Label(frame_parameter, bg=ORANGE, fg=WHITE, text=text).place(x=10, y=10+c)
    c+=50

in_red        = tkinter.Entry(frame_parameter, width=20)
in_green      = tkinter.Entry(frame_parameter, width=20)
in_blue       = tkinter.Entry(frame_parameter, width=20)
in_glcm       = tkinter.Entry(frame_parameter, width=20)
in_hue        = tkinter.Entry(frame_parameter, width=20)
in_saturation = tkinter.Entry(frame_parameter, width=18)
in_value      = tkinter.Entry(frame_parameter, width=18)

# HISTOGRAM FRAME
frame_histogram = tkinter.Frame(root, bg=ORANGE, width=350, height=350)
frame_histogram.place(x=820, y=40)

# INFORMATION FRAME
frame_information = tkinter.Frame(root, bg=ORANGE, width=350, height=170)
frame_information.place(x=40, y=490)

c = 0
for text in ["filename", "filesize", "format"]:
    tkinter.Label(frame_information, bg=ORANGE, fg=WHITE, text=text).place(x=10, y=10+c)
    c+=50

in_filename = tkinter.Entry(frame_information, width=20)
in_filesize = tkinter.Entry(frame_information, width=20)
in_format   = tkinter.Entry(frame_information, width=20)

# IMAGE
sizeImg = 350
image = Image.open("insertimg.png")
image = image.resize((sizeImg, sizeImg))
image = ImageTk.PhotoImage(image)

image1 = tkinter.Label(image=image)
image1.image = image

# PLACEMENT
but_load_image.place(x = 40, y = 420)
but_save_data.place(x = 250, y = 420)

but_prev.place(x=590, y=24)
but_next.place(x=678, y=24)
but_export.place(x=590, y=74)

in_red.place(x=100, y=13)
in_green.place(x=100, y=63)
in_blue.place(x=100, y=113)
in_glcm.place(x=100, y=163)
in_hue.place(x=100, y=213)
in_saturation.place(x=120, y=263)
in_value.place(x=120, y=313)

in_filename.place(x=100, y=13)
in_filesize.place(x=100, y=63)
in_format.place(x=100, y=113)

image1.place(x=40, y=40)


root.mainloop()
