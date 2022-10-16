from tkinter import END, BooleanVar, Button, Canvas, Checkbutton, Entry, Label, Tk, PhotoImage, messagebox, simpledialog
from random import choice, randint, shuffle
import pyperclip
import json

LETTERS_LO = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split()
LETTERS_UP = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
NUMBERS = "0 1 2 3 4 5 6 7 8 9".split()
SYMBOLS = "! ? @ # & * % $ ^".split()
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_generation():
    # removes any previous password from the field
    password_entry.delete(0, END)

    # list comprehension to randomly generate upper/lower letter, numbers and symbols
    password_letters_lo = [choice(LETTERS_LO)
                           for _ in range(randint(4, 6))]
    password_letters_up = [choice(LETTERS_UP)
                           for _ in range(randint(4, 6))]
    password_numbers = [choice(NUMBERS) for _ in range(randint(2, 4))]
    password_symbols = [choice(SYMBOLS) for _ in range(randint(2, 4))]

    # combining the 4 lists into one & shuffling the characters up
    password_values = password_letters_lo + \
        password_letters_up + password_numbers + password_symbols
    shuffle(password_values)

    # making a string of the list of characters & inserting it into the field & auto copying to the clipboard
    generated_password = "".join(password_values)
    password_entry.insert(0, generated_password)
    pyperclip.copy(generated_password)

# ---------------------------- HIDE AND SHOW PASSWORD FIELD ------------------------------- #


def view_password():
    # the function that will allow the checkbox to switch the password field from showing * or the actual characters
    if show_password_value.get():
        password_entry.config(show="*")
    else:
        password_entry.config(show="")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_info():
    # getting the input values from the entry fields
    # capitalizing the website so it si always the same
    website = web_entry.get().capitalize()
    name = name_entry.get()
    password = password_entry.get()

    # basically the new data schema
    new_data = {
        website: [
            {
                "email": name,
                "password": password
            }
        ]
    }

    # strip the entries of whitespace and check if they are empty strings to make sure values are actually added
    if website.strip() == "" or password.strip() == "":
        messagebox.showinfo(title="Empty Field", message="Whoops!",
                            detail="Don't leave any fields empty!")
    else:
        try:
            # try to open the json file as read and load
            with open("data.json", "r") as data_file:
                # Read the data found
                data = json.load(data_file)
        except FileNotFoundError:
            # if file now found it will dump the info put into a file it creates
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Update the data with the new stuff
            data.update(new_data)

            # open with read and ability to append the file at the same time
            with open("data.json", "r+") as data_file:
                # read the current data in the file
                current_data = json.load(data_file)

                # searches for the website inputted within the file
                if website in current_data:
                    # check if within the website found to see if the email used is already stored in the list stored info
                    if not any(emails["email"] == name for emails in current_data[website]):
                        # if the email isn't found at all the current data is appended and added to the list for the emails
                        current_data[website].append(
                            {"email": data[website][0]["email"], "password": data[website][0]["password"]})
                        data_file.seek(0)
                        json.dump(current_data, data_file, indent=4)
                    else:
                        # if the email is found in the list of already saved items of the website the popup message will show to confirm overwrite or cancel to stop
                        overwrite = messagebox.askyesno(
                            title="Overwrite", message=f"Info was already saved for {website} and {name}", detail=f"Would you like to update it?\n\nYes: overwrite the current password\n\nNo: cancel the save and clear the inputs to try again", parent=window)

                        if overwrite == True:
                            # find where in the list of info for that website the data is stored
                            stored_location_find = [index for (index, item) in enumerate(
                                current_data[website]) if item["email"] == name]

                            # change that stored location list to an integer
                            stored_location = int(
                                "".join(map(str, stored_location_find)))

                            # change the password of the specific info
                            current_data[website][stored_location]["password"] = password

                            with open("data.json", "w") as data_file:
                                json.dump(current_data, data_file, indent=4)
                else:
                    # when the website isn't already found just add to the file
                    with open("data.json", "w") as data_file:
                        # Save the new data
                        json.dump(data, data_file, indent=4)
        finally:
            # clear the input fields after saving or canceling the save
            web_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    # get the website input for the search
    website = web_entry.get().capitalize()

    try:
        # try to open the data file where is should be
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        # if the file hasn't been made yet this pop up will show, it should only show because passwords have never been saved
        messagebox.showinfo(title="Search Issue",
                            message="No data file found!", parent=window)
    else:
        # check if the website being searched for is in the file
        if website in data:
            # For when more than one password/email has been saved
            if len(data[website]) > 1:
                # give the list of saved info index values and put those into a list
                find_web_info = [index for (
                    index, item) in enumerate(data[website])]

                # use the index list from before to create a list with a numerical value to be selected
                found_info = ["(" + str(value + 1) + ")" + " " + data[website][value]["email"] for value in find_web_info]

                # creating a string list to put in a message box
                found_info_string = "\n".join(found_info)

                # a message box looking for number input from user to select which email to get a password for
                answer = simpledialog.askinteger(title="Multiple Emails Found", prompt=f"Select which {website} email to get the password:\n\n{found_info_string}\n", parent=window)

                # handles if the user cancels the prompt because it will return none and subtraction can't be done on none
                if answer is not None:
                    answer_value = answer - 1
                
                    # show the selected email and password
                    messagebox.showinfo(title="Found Info", message=f"{website}", detail=f"Email: {data[website][answer_value]['email']}\nPassword: {data[website][answer_value]['password']}", parent=window)
            else:
                # if the site has only one email/password saved to it at this point
                messagebox.showinfo(
                    title="Found Info", message=f"{website}", detail=f"Email: {data[website][0]['email']}\nPassword: {data[website][0]['password']}", parent=window)
        else:
            # when the site doesn't have anything saved for it
            messagebox.showinfo(title="Search Issue",
                                message=f"No passwords for {website} found.", parent=window)

# ---------------------------- UI SETUP ------------------------------- #


# create the window of the program
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# add the background image and place in the specific spot
bg_photo = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(105, 100, image=bg_photo)
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
search_button = Button(text="Search", command=find_password)

show_password_value = BooleanVar(value=True)
show_password = Checkbutton(text="Show", onvalue=False, offvalue=True,
                            command=view_password, variable=show_password_value)


password_button_gen.grid(column=1, row=4, columnspan=2)
password_button_add.grid(column=1, row=5, columnspan=2)
show_password.grid(column=2, row=3)
search_button.grid(column=2, row=1)


window.mainloop()
