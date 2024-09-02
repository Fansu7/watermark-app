import os.path
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageFont, Image, ImageTk, ImageOps, UnidentifiedImageError, ImageDraw
import time

window = tk.Tk()

window.title("Pontelabs Water Mark APP")
window.geometry('512x512')
window.resizable(width=True, height=True)

img_path = None
watermark_text = None

#Select the image we want to watermark
def load_image():
    global img_path
    img_path = filedialog.askopenfilename(initialdir='/home/alvito/Pictures')
    btn_mark_img.config(state="normal")


def close_window():
    window.destroy()


def add_watermark(img_path):
    try:
        watermark_color_pattern = (255, 255, 255, 80)
        file = Image.open(f"{img_path}")
        image = file.convert('RGBA')
        width, height = image.size
        overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        #The image selected will always be watermarked with diagonal lines that we draw with a for loop.
        for i in range(0, width + height, 50):
            draw.line([(0, height - i), (i, height)], fill=watermark_color_pattern, width=5)

        image_width, image_height = image.size

        if click.get() == "Logo":
            #Select the logo we want to "draw" in or image (it should be a PNG)
            mark_image = Image.open(filedialog.askopenfilename(initialdir=f'/home/{os.getlogin()}/Pictures'))
            mark_image = mark_image.convert('RGBA')

            #Resize the logo we'll use as watermark (change if needed).
            mark_image = mark_image.resize((int(image_width * 0.5), int(image_height * 0.5)))
            mark_width, mark_height = mark_image.size

            # calculate the middle of the image we want to watermark to draw the logo in that position.
            x = int((image_width / 2) - (mark_width / 2))
            y = int((image_height / 2) - (mark_height / 2))

            image.paste(mark_image, (x, y), mark_image)

            image = Image.alpha_composite(image, overlay)
            file = filedialog.asksaveasfile(mode='w', defaultextension=".png",
                                            filetypes=(("PNG file", "*.png"), ("All Files", "*.*")))
            save_path = os.path.abspath(file.name)
            image.save(save_path)
            image.show()
            time.sleep(2)
            messagebox.showinfo("Success!", f"Image watermarked successfully.\n Saved in {save_path}")
        elif click.get() == "Text":
                #get w/e the user wrote in the text field
                watermark_text = text_entry.get()
                font_size = 200
                font = ImageFont.truetype('arial.ttf', font_size)

                text_width = draw.textlength(watermark_text, font=font)
                text_height = font_size

                #calculate the middle of the image we want to watermark to draw the text in that position.
                x = int((image_width - text_width) // 2)

                y = int((image_height / 2) - (text_height / 2))

                draw.text((x, y), watermark_text, fill=watermark_color_pattern, font=font)

                image = Image.alpha_composite(image, overlay)
                file = filedialog.asksaveasfile(mode='w', defaultextension=".png", filetypes=(("PNG file", "*.png"),("All Files", "*.*") ))
                save_path = os.path.abspath(file.name)
                image.save(save_path)
    except  (FileNotFoundError, UnidentifiedImageError):
        messagebox.showinfo("Error", "Sorry, something went wrong.")


#if we select the option to watermark with a logo, we'll disable the text field.
def enable_button(option):
    if option == "Logo":
        btn_load_img.config(state="normal")
        text_entry.delete(0, len(text_entry.get()))
        text_entry.config(state="disabled")


bg = ImageTk.PhotoImage(Image.open("pontelabs.jpg"))
canvas = tk.Canvas(window, width=512, height=512)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg, anchor="nw")
options = ["Text", "Logo"]
click = tk.StringVar()
# initial menu text
click.set("Text")

option_menu = tk.OptionMenu(window, click, *options, command=enable_button)
text_entry = tk.Entry()
btn_load_img = tk.Button(window, text="Load image", command=load_image)
btn_mark_img = tk.Button(window, text="Mark image", command=lambda: add_watermark(img_path), borderwidth=3, state="disabled")
btn_exit = tk.Button(window, text="Exit", command=close_window)

option_menu_canvas = canvas.create_window(60, 370, window=option_menu, width=100)
text_entry_canvas = canvas.create_window(60, 410, window=text_entry, width=100)
btn_load_img_canvas = canvas.create_window(60, 450, window=btn_load_img, width=100)
btn_mark_img_canvas = canvas.create_window(60, 490, window=btn_mark_img, width=100)
btn_exit_canvas = canvas.create_window(450, 490, window=btn_exit, width=100)


window.mainloop()
