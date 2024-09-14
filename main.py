from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# Necessary package installation #######################################################################################
import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


########################################################################################################################


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pass():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    letter = [random.choice(letters) for _ in range(nr_letters)]
    symbol = [random.choice(symbols) for _ in range(nr_symbols)]
    number = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = letter + symbol + number

    random.shuffle(password_list)

    generated_password = ''.join(password_list)

    password_entry.insert(0, generated_password)
    # messagebox.showinfo(message='Password copied to clipboard')
    pyperclip.copy(generated_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    if website_entry.get() == '' or mail_entry.get() == '' or password_entry.get() == '':
        messagebox.showerror(title='Invalid entry', message="Do not leave any field empty!")

    else:
        is_ok = messagebox.askyesno(title=website_entry.get().title(), message="These are the details entered\n"
                                                                       f"Website: {website_entry.get().title()}\n"
                                                                       f"Email/Username: {mail_entry.get()}\n"
                                                                       f"Password: {password_entry.get()}\n"
                                                                       f"Is it ok to save?")
        new_data = {
            website_entry.get().title(): {
                'mail': mail_entry.get(),
                'password': password_entry.get()
            }
        }
        if is_ok:
            try:
                with open('data.json', mode='r') as data_file:
                    # Reading the json file
                    data = json.load(data_file)

            except FileNotFoundError:
                with open('data.json', mode='w') as data_file:
                    json.dump(new_data, data_file, indent=4)

            except json.decoder.JSONDecodeError:
                with open('data.json', mode='w') as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                # Updating the json file's data
                data.update(new_data)
                with open('data.json', mode='w') as data_file:
                    # Dumping the json file with the updated data
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, 'end')
                password_entry.delete(0, 'end')


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website_name = website_entry.get().title()
    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title='Error', message='No data file found')
    except json.decoder.JSONDecodeError:
        messagebox.showerror(title='Error', message='No data file found')
    else:
        if website_name in data:
            mail_id = data[website_name]['mail']
            password_of_website = data[website_name]['password']
            messagebox.showinfo(title=website_name, message=f'Email: {mail_id}\nPassword: {password_of_website}')
            pyperclip.copy(password_of_website)
        else:
            messagebox.showerror(title='Error', message=f"No information about website '{website_name}' found")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

# -------------------------------- LOGO -------------------------------- #
canvas = Canvas(width=200, height=189)
lock_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# -------------------------------- Website  -------------------------------- #

website = Label(text='Website:')
website.grid(column=0, row=1, padx=5, pady=5)
website_entry = Entry(width=55)
website_entry.grid(column=1, row=1)
website_entry.focus()

# -------------------------------- Email/Username  -------------------------------- #

mail = Label(text='Email/Username:')
mail.grid(column=0, row=2, padx=5, pady=5)
mail_entry = Entry(width=75)
mail_entry.insert(0, 'akshat.kumar05j@gmail.com')
mail_entry.grid(column=1, row=2, columnspan=2)

# -------------------------------- Password  -------------------------------- #

password = Label(text="Password:")
password.grid(column=0, row=3, padx=5, pady=5)
password_entry = Entry(width=55)
password_entry.grid(column=1, row=3)

generate = Button(text='Generate Password', command=generate_pass)
generate.grid(column=2, row=3, padx=5)

# -------------------------------- Add button  -------------------------------- #

add = Button(text='Add', width=60, command=save)
add.grid(column=1, row=4, columnspan=2)

# -------------------------------- Search -------------------------------- #

search_button = Button(text='Search', padx=12, width=10, command=find_password)
search_button.grid(column=2, row=1)


window.mainloop()
