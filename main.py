import customtkinter
from tkinter import filedialog
from stegano import lsb
from tkinter import messagebox


# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("Dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("dark-blue")


class SteganographyApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("MII")
        self.geometry("400x250")
        self.eval('tk::PlaceWindow . center')
        self.font = 'Roboto', 20

        self.input_text = customtkinter.StringVar()
        self.image_path = ""
        self.image_filename = customtkinter.StringVar()

        self.input_entry = customtkinter.CTkEntry(self,
                                                  textvariable=self.input_text,
                                                  font=self.font,
                                                  text_color="grey65",
                                                  width=10)

        self.hide_button = customtkinter.CTkButton(self, text="Hide",
                                                   command=self.hide_text,
                                                   font=self.font,
                                                   cursor='hand2')
        # self.show_label = customtkinter.CTkLabel(self, text="Revealed text:")
        self.show_button = customtkinter.CTkButton(self, text="Show",
                                                   command=self.show_text,
                                                   font=self.font,
                                                   cursor='hand2')
        self.load_button = customtkinter.CTkButton(self, text="Load Image",
                                                   command=self.load_image,
                                                   font=self.font,
                                                   cursor='hand2')
        self.save_button = customtkinter.CTkButton(self, text="Save Image",
                                                   command=self.save_image,
                                                   font=self.font,
                                                   cursor='hand2')
        self.file_label = customtkinter.CTkLabel(self,
                                                 textvariable=self.image_filename,
                                                 font=("Roboto", 10),
                                                 text_color="grey45")

        self.input_entry.pack(ipady=3, padx=10, pady=10, fill='x')
        self.input_entry.focus_get()
        self.hide_button.pack(ipady=5, padx=10, pady=2, fill='x')
        self.show_button.pack(ipady=5, padx=10, pady=2, fill='x')
        self.load_button.pack(ipady=5, padx=10, pady=2, fill='x')
        self.save_button.pack(ipady=5, padx=10, pady=2, fill='x')
        self.file_label.pack(anchor='se', padx=10, pady=2)

    def hide_text(self):
        text = self.input_text.get()
        if self.image_path == "":
            self.load_image()
        if self.image_path != "":
            secret = lsb.hide(self.image_path, text)
            secret.save(self.image_path)
            messagebox.showinfo("Success",
                                "Text successfully hidden in the image.")
            self.input_entry.delete(0, 'end')

    def show_text(self):
        if self.image_path == "":
            self.load_image()
        if self.image_path != "":
            secret = lsb.reveal(self.image_path)
            self.input_text.set(secret)

    def load_image(self):
        self.image_path = filedialog.askopenfilename(initialdir="/",
                                                     title="Select file",
                                                     filetypes=(
                                                         ("all files", "*.*"),
                                                         ("png files", "*.png"),
                                                         ("jpeg files", "*.jpg")
                                                     ))
        self.image_filename.set(self.image_path.split("/")[-1])

    def save_image(self):
        file_path = filedialog.asksaveasfilename(initialdir="/Desktop",
                                                 title="Select file",
                                                 filetypes=(
                                                     ("png files", "*.png"),
                                                     ("all files", "*.*")))
        if file_path:
            secret = lsb.hide(self.image_path, self.input_text.get())
            secret.save(file_path)
            self.input_entry.delete(0, 'end')
            messagebox.showinfo("Success", "Image successfully saved.")


# Cut / Paste / Copy function
def on_key_release(event):
    ctrl = (event.state & 0x4) != 0
    if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")

    if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")

    if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

    if event.keycode == 65 and ctrl and event.keysym.lower() != "a":
        event.widget.select_range(0, 'end')


app = SteganographyApp()
app.bind_all("<Key>", on_key_release, "+")
app.mainloop()
