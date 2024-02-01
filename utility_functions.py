from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import filedialog, messagebox
from tkinter.messagebox import showinfo


# Simple way to store variables
class VarStorage:
    def __init__(self):
        self._keep_variable = None

    def set_variable(self, x):
        self._keep_variable = x

    def get_variable(self):
        return self._keep_variable


# Creating instances of VarStorage
temp_var = VarStorage()
temp_var_pil = VarStorage()
temp_var_keep = VarStorage()


class WatermarkUtility:
    def __init__(self, font_cb, opacity_cb, size_cb, color_cb, wm_entry, location_cb):
        self.FONT_NAME = "arial"
        self.SIZE = 50
        self.COLOR = (255, 255, 255)
        self.OPACITY = (255,)
        self.LOCATION = (10, 10)
        self.font_cb = font_cb
        self.opacity_cb = opacity_cb
        self.size_cb = size_cb
        self.color_cb = color_cb
        self.wm_entry = wm_entry
        self.location_cb = location_cb

    def scale_image(self, image_passed):
        upper_width = 900
        middle_width = 700
        lower_width = 500

        if image_passed.size[0] >= image_passed.size[1]:
            if image_passed.size[0] <= middle_width:
                base_width = image_passed.size[0]
            else:
                base_width = upper_width
        else:
            if image_passed.size[1] <= lower_width:
                base_width = image_passed.size[0]
            else:
                base_width = middle_width

        width_percent = (base_width / float(image_passed.size[0]))
        height_size = int(float(image_passed.size[1]) * float(width_percent))
        return image_passed.resize((base_width, height_size), Image.LANCZOS)

    def file_selection(self, image_area):
        filetypes = [('image files', ('.png', '.jpg')), ('All files', '*.*')]
        filename = filedialog.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)

        if not filename:
            return

        messagebox.showinfo(title='Selected File', message=filename)

        # Open image with PIL
        img = Image.open(filename)

        # Temp variable for later adjustment of watermark
        temp_var_pil.set_variable(img)

        tk_img = ImageTk.PhotoImage(self.scale_image(img))
        temp_var.set_variable(tk_img)
        image_area.config(image=temp_var.get_variable(),
                          width=self.scale_image(img).size[0],
                          height=self.scale_image(img).size[1])

    def font_selection(self, selected_font):
        font_dict = {
            "Arial": "arial",
            "Arial Italic": "ariali",
            "Arial Bold": "arialbd",
            "Arial Black": "ariblk",
            "Impact": "impact",
            "Calibri": "calibri",
            "Calibri Italic": "calibrii",
            "Calibri Bold": "calibrib",
            "Calibri Bold Italic": "calibriz",
            # Add more fonts as needed
        }

        # print(f"Got Self.FONT_NAME: {selected_font}")
        self.FONT_NAME = font_dict.get(selected_font, "arial")

    def size_selection(self, selected_size):
        self.SIZE = int(selected_size)
        # print(f"Got Self.SIZE: {self.SIZE}")

    def color_selection(self, selected_color):
        color_dict = {'Black': (0, 0, 0), 'Gray': (160, 160, 160), 'Brown': (102, 51, 0), 'Blue': (0, 128, 255),
                      'Purple': (153, 51, 255),
                      'Green': (0, 153, 76), 'Red': (255, 0, 0), 'Yellow': (255, 255, 0), 'White': (255, 255, 255),
                      'Silver': (192, 192, 192),
                      'Gold': (255, 153, 51), 'Orange': (255, 128, 0)}
        self.COLOR = color_dict[selected_color]  # adding a default color in case of errors
        # print(f"Got Self.COLOR: {self.COLOR}")

    def opacity_selection(self, selected_opacity):
        selected_opacity = int(selected_opacity)
        opacity_dict = {100: (255,), 75: (192,), 50: (127,), 25: (65,), 0: (0,)}
        self.OPACITY = opacity_dict[selected_opacity]
        # print(f"Got Self.OPACITY: {self.OPACITY}")

    def location_selection(self, selected_location):
        self.LOCATION = selected_location

    def calculate_text_position(self, img, text_width, text_height, margin, selected_location):
        position_mapping = {
            "Top Left": (margin, margin),
            "Top": ((img.width - text_width) // 2, margin),
            "Top Right": (img.width - text_width - margin, margin),
            "Center Left": (margin, (img.height - text_height) // 2),
            "Center": ((img.width - text_width) // 2, (img.height - text_height) // 2),
            "Center Right": (img.width - text_width - margin, (img.height - text_height) // 2),
            "Bottom Left": (margin, img.height - text_height - margin),
            "Bottom": ((img.width - text_width) // 2, img.height - text_height - margin),
            "Bottom Right": (img.width - text_width - margin, img.height - text_height - margin),
        }

        return position_mapping.get(selected_location, (0, 0))

    def draw_watermark(self, img):
        img = img.convert('RGBA')
        margin = 10
        opaque_img = Image.new('RGBA', img.size, (255, 255, 255, 0))

        draw = ImageDraw.Draw(opaque_img)
        text = self.wm_entry.get()

        font = ImageFont.truetype(self.FONT_NAME, self.SIZE)
        txt_size = draw.textbbox((0, 0), text, font)
        text_height = txt_size[3]
        text_width = txt_size[2] - txt_size[0]

        x, y = self.calculate_text_position(img, text_width, text_height, margin, selected_location=self.LOCATION)

        draw.text((x, y), text, font=font, fill=self.COLOR + self.OPACITY)

        combined = Image.alpha_composite(img, opaque_img)

        # Saving this Variable to be used when the save method is called by user
        temp_var_keep.set_variable(combined.convert('RGB'))

        return combined

    def apply_watermark(self, image_area):
        img = temp_var_pil.get_variable()
        watermark_img = self.draw_watermark(img)
        self.update_display(watermark_img, image_area)

    def update_display(self, img, image_area):
        tk_img = ImageTk.PhotoImage(self.scale_image(img))
        temp_var.set_variable(tk_img)
        image_area.config(
            image=temp_var.get_variable(),
            width=self.scale_image(img).width,
            height=self.scale_image(img).height
        )

    def confirm_button_pressed(self, image_area):
        # Call the three methods
        img = temp_var_pil.get_variable()

        if img is None:
            showinfo(title='Warning', message='Please upload a file first')
            return

        self.apply_watermark(image_area)
        # apply_watermark -> draw_watermark -> update_display

    def reset_settings(self):
        self.font_cb.current(0)
        self.opacity_cb.current(0)
        self.size_cb.current(7)
        self.location_cb.current(6)
        self.color_cb.current(9)
        self.wm_entry.delete(0, 'end')
        self.wm_entry.insert(0, "@Your_Handle")
        self.FONT_NAME = "arial"
        self.SIZE = 90
        self.COLOR = (255, 255, 255)
        self.OPACITY = (255,)

    def save(self):
        file = filedialog.asksaveasfile(
            mode='w',
            defaultextension='*.*',
            filetypes=(('JPG file', '*.jpg'), ('PNG file', '*.png'), ('All files', '*.*'))
        )
        if file:
            watermarked_image = temp_var_keep.get_variable()
            if watermarked_image is not None:
                watermarked_image.save(file.name)

    def help_message(self):
        messagebox.showinfo(title="Help",
                            message="Welcome to Help!\n\nFirst: Upload photo with Open button(Must be .jpg or .png).\n"
                                    "\nSecond: Write text for your watermark - maybe your @handle\n"
                                    "\nThird: Choose your desired font, size, opacity, and text location\n"
                                    "\nFinally: Use the Save button to save the watermarked picture to a new file.\n"
                                    "\npsssst - the Reset Values button will help you return the settings to default"
                            )

    def about_message(self):
        messagebox.showinfo(title="About this app",
                            message="This is my take on a watermarking app. I utilize the color Orange because I truly"
                                    " love the color. I am a new software developer that enjoys learning by doing. "
                                    "Feel free to use this app, whether as a Watermarking tool, or build your own"
                                    " rendition with my app as a starting point! Enjoy!")
