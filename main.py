import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from utility_functions import WatermarkUtility


class WatermarkApp:
    def __init__(self, main_window, watermark_utility):
        # Main window and Image area config
        self.root = main_window
        self.root.title("Water Marking With Michael")
        self.root.config(padx=20, pady=20, bg="#FFDEAD")
        self.alien_logo_img = ImageTk.PhotoImage(Image.open("orange_alien2.png"))
        self.image_area = tk.Label(width=130, height=40)
        self.image_area.grid(padx=5, pady=10, rowspan=5, row=0, column=1, columnspan=7)
        self.wm_entry = tk.Entry(width=20)

        # starting values for setting widgets
        self.selected_font = tk.StringVar()
        self.font_cb = ttk.Combobox(textvariable=self.selected_font)
        self.selected_size = tk.IntVar()
        self.size_cb = ttk.Combobox(textvariable=self.selected_size)
        self.selected_color = tk.StringVar()
        self.color_cb = ttk.Combobox(textvariable=self.selected_color)
        self.selected_opacity = tk.IntVar()
        self.opacity_cb = ttk.Combobox(textvariable=self.selected_opacity)
        self.selected_orientation = tk.StringVar()
        self.location_cb = ttk.Combobox(textvariable=self.selected_orientation)

        self.wmu = watermark_utility
        self.create_column_0()
        self.create_column_2()
        self.create_column_3()
        self.create_column_4()
        self.create_column_6()

    def create_column_0(self):
        # Column 0 - Left Side
        canvas = tk.Canvas(width=150, height=150, bg="#FFDEAD", highlightthickness=0)
        canvas.create_image(75, 75, image=self.alien_logo_img)
        canvas.grid(row=0, column=0)

        file_options_label = tk.Label(text="File Options:", bg='#FFDEAD')
        file_options_label.grid(row=2, column=0, sticky="NE", padx=(0, 50))

        open_button = tk.Button(width=12, text="Open", command=lambda: self.wmu.file_selection(self.image_area))
        open_button.grid(row=3, column=0)

        save_button = tk.Button(width=12, text="Save", command=self.wmu.save)
        save_button.grid(row=4, column=0, pady=(0, 400))

        instruction_label = tk.Label(text="Watermark Text:", bg='#FFDEAD')
        instruction_label.grid(row=5, column=0)

        wm_entry.insert(0, "@Your_Handle")
        wm_entry.grid(row=6, column=0)

        help_button = tk.Button(width=12, text="Help", command=wmu.help_message)
        help_button.grid(row=7, column=0, pady=(10, 0))

        about_button = tk.Button(width=12, text="About", command=wmu.about_message)
        about_button.grid(row=8, column=0)

    def create_column_2(self):
        # Column 2 Bottom Settings
        font_label = tk.Label(text="Font:", bg='#FFDEAD')
        font_label.grid(row=5, column=2, sticky="W")

        font_cb['values'] = [
            "Arial",
            "Arial Italic",
            "Arial Bold",
            "Arial Black",
            "Impact",
            "Calibri",
            "Calibri Italic",
            "Calibri Bold",
            "Calibri Bold Italic",
        ]

        # prevent typing a value
        font_cb['state'] = 'readonly'
        font_cb.current(0)
        font_cb.grid(row=6, column=2, sticky="W")

        def on_font_selection(event):
            selected_font_name = font_cb.get()
            # print(f"Selected Font: {selected_font_name}")
            wmu.font_selection(selected_font_name)

        font_cb.bind('<<ComboboxSelected>>', on_font_selection)

        size_label = tk.Label(text="Font Size:", bg='#FFDEAD')
        size_label.grid(row=7, column=2, pady=(20, 0), sticky="W")

        # get first 3 letters of every month name
        size_cb['values'] = [10, 20, 30, 40, 50, 60, 70, 90, 100]
        # prevent typing a value
        size_cb['state'] = 'readonly'
        size_cb.current(4)
        size_cb.grid(row=8, column=2, sticky="W")

        def on_size_selection(event):
            selected_font_size = size_cb.get()
            # print(f"Selected Font Size: {selected_font_size}")
            wmu.size_selection(selected_font_size)

        size_cb.bind('<<ComboboxSelected>>', on_size_selection)

    def create_column_3(self):
        # Column 3
        color_label = tk.Label(text="Color:", bg='#FFDEAD')
        color_label.grid(row=5, column=3, sticky="W")

        # get first 3 letters of every month name
        color_cb['values'] = ['Black', 'Gray', 'Brown', 'Blue', 'Purple', 'Green', 'Red', 'Orange', 'Yellow', 'White',
                              'Silver', 'Gold']
        # prevent typing a value
        color_cb['state'] = 'readonly'
        color_cb.current(9)
        color_cb.grid(row=6, column=3, sticky="W")

        def on_color_selection(event):
            selected_color = color_cb.get()
            # print(f"Selected color: {selected_color}")
            wmu.color_selection(selected_color)

        color_cb.bind('<<ComboboxSelected>>', on_color_selection)

        opacity_label = tk.Label(text="Opacity:", bg='#FFDEAD')
        opacity_label.grid(row=7, column=3, pady=(20, 0), sticky="W")
        opacity_cb['values'] = [100, 75, 50, 25, 0]
        # prevent typing a value
        opacity_cb['state'] = 'readonly'
        opacity_cb.current(0)
        opacity_cb.grid(row=8, column=3, sticky="W")

        def on_opacity_selection(event):
            selected_opacity = opacity_cb.get()
            # print(f"Selected Font Size: {selected_opacity}")
            wmu.opacity_selection(selected_opacity)

        opacity_cb.bind('<<ComboboxSelected>>', on_opacity_selection)

    def create_column_4(self):
        # Column 4
        orientation_label = tk.Label(text="Text Location:", bg='#FFDEAD')
        orientation_label.grid(row=5, column=4, sticky="W")

        location_cb['values'] = ['Top Left', 'Top', 'Top Right', 'Center Left', 'Center', 'Center Right',
                                 'Bottom Left', 'Bottom', 'Bottom Right']
        # prevent typing a value
        location_cb['state'] = 'readonly'
        location_cb.current(0)
        location_cb.grid(row=6, column=4, sticky="W")

        def on_location_selection(event):
            selected_location = location_cb.get()
            # print(f"Selected Text Location: {selected_location}")
            wmu.location_selection(selected_location)

        location_cb.bind('<<ComboboxSelected>>', on_location_selection)

    def create_column_6(self):
        # Column 6
        apply_label = tk.Label(text="Apply Changes:", bg='#FFDEAD')
        apply_label.grid(row=5, column=6, sticky="E")

        confirm_button = tk.Button(width=10, text="Confirm",
                                   command=lambda: wmu.confirm_button_pressed(self.image_area))
        confirm_button.grid(row=6, column=6, sticky="E")

        reset_label = tk.Label(text="Reset Values:", bg='#FFDEAD')
        reset_label.grid(row=7, column=6, pady=(20, 0), sticky="E")

        reset_button = tk.Button(width=10, text="Reset", command=wmu.reset_settings)
        reset_button.grid(row=8, column=6, sticky="E")


if __name__ == "__main__":
    root = tk.Tk()

    # Create widgets
    font_cb = ttk.Combobox()
    opacity_cb = ttk.Combobox()
    size_cb = ttk.Combobox()
    color_cb = ttk.Combobox()
    wm_entry = tk.Entry()
    location_cb = ttk.Combobox()

    # Pass widgets to WatermarkUtility
    wmu = WatermarkUtility(font_cb, opacity_cb, size_cb, color_cb, wm_entry, location_cb)
    app = WatermarkApp(root, wmu)

    root.mainloop()
