import os
import imageio
import customtkinter
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Battlezone DDS Creator")
        self.geometry("900x600")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "gui")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "nsdf_star.png")),
                                                 size=(26, 26))
        self.large_bzone_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "bzone_blank.png")),
                                                        size=(386, 32))
        self.small_bzone_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "bzone_blank.png")),
                                                        size=(96, 8))
        self.tab_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "images.png")),
                                                size=(20, 20))
        self.empty_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "no_img.png")),
                                                  size=(200, 200))
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  DDS Creator",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Convert to DDS",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.tab_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.navigation_frame_bz_image = customtkinter.CTkLabel(self.navigation_frame, text="",
                                                                image=self.small_bzone_image)
        self.navigation_frame_bz_image.grid(row=6, column=0, pady=20)

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_left = customtkinter.CTkFrame(self.home_frame, corner_radius=40)
        self.home_frame_left.grid(row=0, column=0, padx=(40, 10), pady=60, sticky="nsew")
        self.home_frame_left.grid_columnconfigure(0, weight=1)

        self.home_frame_right = customtkinter.CTkFrame(self.home_frame, corner_radius=40)
        self.home_frame_right.grid(row=0, column=1, padx=(10, 40), pady=60, sticky="nsew")
        self.home_frame_right.grid_columnconfigure(0, weight=1)

        """
        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="",
                                                                   image=self.large_bzone_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=50)
        """

        self.image_file_label = customtkinter.CTkLabel(self.home_frame_left, text="No file selected!",
                                                       font=customtkinter.CTkFont(size=14, weight="bold"))
        self.image_file_label.grid(row=2, column=0, padx=20, pady=(40, 10))

        self.browse_button = customtkinter.CTkButton(self.home_frame_left, text="Browse for Image",
                                                     corner_radius=20,
                                                     fg_color="#39424a", hover_color="#4b5a69",
                                                     command=self.browse_file)
        self.browse_button.grid(row=3, column=0, padx=20, pady=10, ipadx=60, ipady=12)

        self.convert_button = customtkinter.CTkButton(self.home_frame_left, text="Convert",
                                                      corner_radius=20,
                                                      border_width=2,
                                                      fg_color="#39424a", hover_color="#4b5a69",
                                                      command=self.convert_to_dds)
        self.convert_button.grid(row=4, column=0, padx=20, pady=10, ipadx=60, ipady=12)

        self.image_selected_label = customtkinter.CTkLabel(self.home_frame_right, text="Selected image:")
        self.image_selected_label.grid(row=5, column=0, padx=20, pady=10)

        # self.image_selected_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=40)
        # self.image_selected_frame.grid(row=6, column=0,  padx=20, pady=10, sticky="nsew")
        # self.image_selected_frame.grid_columnconfigure(1, weight=1)

        self.image_label = customtkinter.CTkLabel(self.home_frame_right, text="", image=self.empty_image)
        self.image_label.grid(row=6, column=0, padx=40, pady=(8, 20), sticky="nsew")

        self.image_selected_label_warn = customtkinter.CTkLabel(self.home_frame_right,
                                                                text="",
                                                                font=customtkinter.CTkFont(size=9, weight="bold"))
        self.image_selected_label_warn.grid(row=7, column=0, padx=20, pady=(4, 10))

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.image_file_label.configure(text=f"Selected file:\n\n{os.path.basename(file_path)}")
        # self.file_path = file_path

        # Display the selected image
        self.display_image(file_path)

    def display_image(self, file_path):
        if file_path:
            """
            image = Image.open(file_path)
            image.thumbnail((200, 200))  # Resize the image for display
            photo = ImageTk.PhotoImage(image)
            """
            photo = customtkinter.CTkImage(Image.open(file_path), size=(200, 200))
            # Update the label to display the image
            self.image_label.configure(image=photo)
            self.image_selected_label_warn.configure(text="* image has been resized to fit preview at 200x200")
            self.image_label.image = photo

    def convert_to_dds(self):
        if hasattr(self, 'file_path'):
            try:
                image = Image.open(self.file_path)
                output_path = self.file_path.rsplit('.', 1)[0] + '.dds'
                imageio.imsave(output_path, image)
                tk.messagebox.showinfo("Conversion Complete", f"Image converted and saved to {output_path}")
            except Exception as e:
                tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            tk.messagebox.showwarning("No File Selected", "Please select an image file first.")


if __name__ == "__main__":
    app = App()
    app.iconbitmap("./gui/nsdf_star.ico")
    app.mainloop()
