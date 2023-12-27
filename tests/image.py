from PIL import Image
import customtkinter

window = customtkinter.CTk()
window.resizable(width=False, height=False)

my_image = customtkinter.CTkImage(light_image=Image.open("D:/FCAI - DU/4th & Final year/4th year 1st term/Parallel Processing/Project/images/test9.jpg"),
                                  dark_image=Image.open("D:/FCAI - DU/4th & Final year/4th year 1st term/Parallel Processing/Project/images/test9.jpg"),
                                  size=(500, 500))

image_label = customtkinter.CTkLabel(window, image=my_image, text="")  # display image with a CTkLabel
image_label.pack()

window.mainloop()