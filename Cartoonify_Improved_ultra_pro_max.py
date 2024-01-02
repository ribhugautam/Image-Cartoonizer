import cv2
import easygui
import numpy as np
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *
from PIL import ImageTk, Image


def upload():
    image_path = easygui.fileopenbox()
    if image_path:
        image_preview_label.config(image=None)  
        process_button.config(state=NORMAL)    
        process_button.image_path = image_path  
        show_image_preview(image_path)

def show_image_preview(image_path):
    img = Image.open(image_path)
    img = img.resize((300, 300), Image.ANTIALIAS)  
    img = ImageTk.PhotoImage(img)
    image_preview_label.config(image=img)
    image_preview_label.image = img

def process():
    image_path = process_button.image_path
    if image_path:
        cartoonify(image_path)

def show_save_frame(cartoon_image, image_path):
    save_frame = tk.Toplevel()
    save_frame.title("Save Image")
    save_frame.geometry("300x350")

    cartoon_preview = Image.fromarray(cartoon_image)
    cartoon_preview = cartoon_preview.resize((200, 150))
    cartoon_preview = ImageTk.PhotoImage(cartoon_preview)
    preview_label = Label(save_frame, image=cartoon_preview)
    preview_label.image = cartoon_preview
    preview_label.pack(pady=10)

    save_button = Button(save_frame, text="Save Cartoon", command=lambda: save(cartoon_image, image_path))
    save_button.config(bg='#00BFFF', fg='white', font=('calibri', 12, 'bold'), relief="solid", padx=20, pady=5)
    save_button.pack(pady=5)

    close_button = Button(save_frame, text="Cancel", command=save_frame.destroy)
    close_button.config(bg='#00BFFF', fg='white', font=('calibri', 12, 'bold'), relief="solid", padx=20, pady=5)
    close_button.pack()

def cartoonify(image_path):
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    if original_image is None:
        messagebox.showerror("Error", "Can not find any image. Choose an appropriate file")
        return

    
    gray_scale_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)

    smooth_gray_scale = cv2.medianBlur(gray_scale_image, 5)
    get_edge = cv2.adaptiveThreshold(smooth_gray_scale, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, 9, 9)

    color_image = cv2.bilateralFilter(original_image, 9, 300, 300)
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=get_edge)

    images = [original_image, gray_scale_image, smooth_gray_scale, get_edge, color_image, cartoon_image]

    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    show_cartoonified_image(cartoon_image, image_path)

def show_cartoonified_image(cartoon_image, image_path):
    plt.imshow(cartoon_image)
    plt.axis('off')

    save1 = Button(top, text="Save", command=lambda: show_save_frame(cartoon_image, image_path))
    save1.config(bg='#00BFFF', fg='white', font=('calibri', 12, 'bold'), relief="solid", padx=20, pady=5)
    save1.pack(side=BOTTOM, pady=30)

    plt.show()

def save(resized6, image_path):
    new_name = "cartoonified_Image"
    path1 = os.path.dirname(image_path)
    extension = os.path.splitext(image_path)[1]
    path = os.path.join(path1, new_name + extension)
    cv2.imwrite(path, cv2.cvtColor(resized6, cv2.COLOR_RGB2BGR))
    message = "Image saved as " + new_name + extension + " at " + path
    messagebox.showinfo("Save Successful", message)


top = tk.Tk()
top.geometry('800x600')
top.title('Cartoonify.Image')
top.configure(background='black')


background_image = Image.open("goku.jpg")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(top, image=background_photo)
background_label.place(relwidth=1, relheight=1)

upload_button_img = Image.open("icon.png")
upload_button_photo = ImageTk.PhotoImage(upload_button_img)
upload_button = Button(top, text="Upload Image", image=upload_button_photo, compound=TOP, command=upload, padx=5, pady=5)
upload_button.config(bd=0, highlightthickness=0)
upload_button.config(bg='#00BFFF', fg='white', font=('calibri', 14, 'bold'), relief="solid", padx=20, pady=10)
upload_button.pack(side=TOP, pady=10)

process_button_img = Image.open("process_icon.png")
process_button_photo = ImageTk.PhotoImage(process_button_img)
process_button = Button(top, text="Process Image", image=process_button_photo, compound=TOP, command=process, padx=5, pady=5)
process_button.config(bd=0, highlightthickness=0)
process_button.config(bg='#00BFFF', fg='white', font=('calibri', 14, 'bold'), relief="solid", padx=20, pady=10)
process_button.pack(side=TOP, pady=5)
process_button.config(state=DISABLED)  

image_preview_label = tk.Label(top)
image_preview_label.pack(side=TOP, pady=20)

top.mainloop()
