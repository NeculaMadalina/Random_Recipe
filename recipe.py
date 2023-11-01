"""Recipe Module
It uses a sql database 'Generator.db' , and returns the result in a tkinter window, showing the name of the recipe,
a picture of it, the link to the recipe and the ability to mix again."""

from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO
import sqlite3
from numpy import random
import webbrowser
import yaml
import sys


def get_yml_data():
    """Function that open a yaml file and get the necessary information."""
    try:
        with open('config.yml', 'r') as fr:
            data = yaml.safe_load(fr)
            return data
    except OSError():
        sys.exit(2)


data_config = get_yml_data()
API_KEY = data_config.get('api_key')
RECIPE_IMAGE_WIDTH = 500
RECIPE_IMAGE_HEIGHT = 300

root = Tk()
root.title('Random Recipe Generator')
# root.eval('tk::PlaceWindow . centre')

frame1 = Frame(root, width=500, height=600, bg='#000000')
frame2 = Frame(root, bg='#040D12')
for frame in (frame1, frame2):
    frame.grid(row=1, column=1, sticky='nsew')


def clear_widgets(frames):
    """Function that helps to clear all the widgets that exist in the other frame."""
    for widgets in frames.winfo_children():
        widgets.destroy()


def fetch_db():
    """Function that helps to access data from database, to iterating them and returns a random one."""
    con = sqlite3.connect('Generator.db')
    cursor = con.cursor()
    cursor.execute('SELECT * FROM Generator;')
    data = cursor.fetchall()
    index = random.randint(0, len(data) - 1)
    info = data[index]
    con.close()
    return info


def get_all_data(info):
    """Function that get the source URL that recipe have with concatenate a URL search with id of recipe and an
    API KEY."""
    id_of_recipe = str(info[0])
    url = 'https://api.spoonacular.com/recipes/' + id_of_recipe + '/information?apiKey=' + API_KEY
    rsp = requests.get(url).json()
    return webbrowser.open(rsp['sourceUrl'])


def load_frame1():
    """Function that holds an introductory widgets, destroys all existing widgets on the other frame
     and helps the user enter on the second frame."""
    clear_widgets(frame2)
    frame1.tkraise()
    frame1.pack_propagate(False)
    logo = requests.get('https://www.foodnavigator.com/var/wrbm_gb_food_pharma/storage/images/publications/food-'
                        'beverage-nutrition/foodnavigator.com/news/science/black-is-back-the-secret-to-getting-people-'
                        'to-buy-more-veg/10012647-1-eng-GB/Black-is-back-The-secret-to-getting-people-to-buy-more-'
                        'veg.jpg')
    img = Image.open(BytesIO(logo.content))
    img = img.resize((RECIPE_IMAGE_WIDTH, RECIPE_IMAGE_HEIGHT))
    immg = ImageTk.PhotoImage(img)
    holder = Label(frame1, image=immg, bg='#000000')
    holder.image = immg
    holder.pack(side='bottom')
    Label(frame1, text='Ready for your random recipe?', bg='#000000', fg='white',
          font=('Lucida Calligraphy', 20)).pack(pady=50)
    Button(frame1, text='SHUFFLE', font=('Felix Titling', 20), bg='#3D0000', fg='white', cursor='hand2',
           activebackground='#3D0000', activeforeground='#000000', command=lambda: load_frame2()).pack()


def load_frame2():
    """Function that holds all the widget with the information of the recipe, destroys all existing widgets on the
    other frame, and a widget that allows to user to go back to the frame one and get another random recipe."""
    clear_widgets(frame1)
    frame2.tkraise()
    info = fetch_db()

    Label(frame2, text=info[1], bg='#183D3D', fg='white', font=('Lucida Calligraphy', 20)).pack(pady=30, padx=10)

    logo = requests.get(info[2])
    img = Image.open(BytesIO(logo.content))
    img = img.resize((350, 300))
    immg = ImageTk.PhotoImage(img)
    holder = Label(frame2, image=immg, bg='#5C8374')
    holder.image = immg
    holder.pack(pady=10)

    Button(frame2, text='Find more about your recipe! Here is the link.', font=('TkHeadingFont', 18), bg='#183D3D',
           fg='white', activebackground='#badee2', activeforeground='black',
           command=lambda: get_all_data(info)).pack(pady=5, padx=10)
    Button(frame2, text='Get back and shuffle again!', font=('TkHeadingFont', 18), bg='#183D3D',
           cursor='hand2', activebackground='#badee2', activeforeground='black',
           command=lambda: load_frame1()).pack(side='bottom', pady=10)


if __name__ == '__main__':
    load_frame1()
    root.mainloop()
