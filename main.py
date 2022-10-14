from tkinter import END, BooleanVar, Button, Canvas, Checkbutton, Entry, Label, Tk, PhotoImage, messagebox
from random import choice, randint, shuffle
import pyperclip
import json

LETTERS = "a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
NUMBERS = "0 1 2 3 4 5 6 7 8 9".split()
SYMBOLS = "! ? @ # : & * % $ ^".split()
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_generation():
    password_entry.delete(0, END)

    password_letters = [choice(LETTERS) for _ in range(randint(8, 10))]
    password_numbers = [choice(NUMBERS) for _ in range(randint(8, 10))]
    password_symbols = [choice(SYMBOLS) for _ in range(randint(8, 10))]

    password_values = password_letters + password_numbers + password_symbols

    shuffle(password_values)

    generated_password = "".join(password_values)

    password_entry.insert(0, generated_password)
    pyperclip.copy(generated_password)

# ---------------------------- HIDE AND SHOW PASSWORD FIELD ------------------------------- #


def view_password():
    if show_password_value.get():
        password_entry.config(show="*")
    else:
        password_entry.config(show="")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_info():
    website = web_entry.get()
    name = name_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": name,
            "password": password
        }
    }

    if website.strip() == "" or password == " ":
        messagebox.showinfo(message="Whoops!",
                            detail="Don't leave any fields empty!")

    else:
        complete_save = messagebox.askokcancel(
            message=website, detail=f"Info to be saved: \nEmail/Username: {name} \nPassword: {password}")

        if complete_save:
            try:
                with open("data.json", "r") as data_file:
                    # Read the data found
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Update the data with the new stuff
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # Save the new data
                    json.dump(data, data_file, indent=4)
            finally:
                web_entry.delete(0, END)
                password_entry.delete(0, END)


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
web_entry = Entry(width=29)

name_entry = Entry(width=38)
name_entry.insert(END, "testing@email.com")

password_entry = Entry(width=29, show="*")

web_entry.grid(column=1, row=1)
name_entry.grid(column=1, row=2, columnspan=2)
password_entry.grid(column=1, row=3)

web_entry.focus()

# buttons
password_button_gen = Button(
    text="Generate Password", width=35, command=password_generation)
password_button_add = Button(text="Add", width=35, command=save_info)
search_button = Button(text="Search")

show_password_value = BooleanVar(value=True)
show_password = Checkbutton(text="Show", onvalue=False, offvalue=True,
                            command=view_password, variable=show_password_value)


password_button_gen.grid(column=1, row=4, columnspan=2)
password_button_add.grid(column=1, row=5, columnspan=2)
show_password.grid(column=2, row=3)
search_button.grid(column=2, row=1)


window.mainloop()
