from tkinter import Tk


root = Tk()

root.geometry("500x500")

background =  Tk.Canvas(root, width=800, height=600)
background.pack(fill="both", expand=True)

background_image_path = image_path = PhotoImage(file= r"C:\Users\Alex\Documents\Beyblade_Program\images\beyblade_emblem.png")
background_image = Image.open(background_image_path)

resize_background = background_image.resize((500,500), background.Resampling.LANCZOS)
bey_background = ImageTk.PhotoImage(resize_background)

canvas.create_image(0,0,image = bey_background, anchor = "nw")


root.mainloop()