from tkinter import Button, Canvas, Entry, Label, Tk, PhotoImage
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# ---------------------------- SAVE PASSWORD ------------------------------- #
with open("passwords.txt") as

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

bg_photo = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(135, 100, image=bg_photo)
canvas.grid(column=1, row=0)

# labels
web_label = Label(text="Website:")
name_label = Label(text="Email/Username:")
password_label = Label(text="Password:")
web_label.grid(column=0, row=1)
name_label.grid(column=0, row=2)
password_label.grid(column=0, row=3)

# entries
web_entry = Entry(width=38)
name_entry = Entry(width=38)
password_entry = Entry(width=21)
web_entry.grid(column=1, row=1, columnspan=2)
name_entry.grid(column=1, row=2, columnspan=2)
password_entry.grid(column=1, row=3)

web_entry.focus()

# buttons
password_button_gen = Button(text="Generate Password")
password_button_add = Button(text="Add", width=36)
password_button_gen.grid(column=2, row=3)
password_button_add.grid(column=1, row=4, columnspan=2)


window.mainloop()
