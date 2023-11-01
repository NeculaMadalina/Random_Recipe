"""Get Data Module
Created a sql database with information coming from an API: 'https://spoonacular.com/food-api',
and returns recipe id, name and image URL of the recipe, each on one column."""

import requests
import sys
import yaml
import sqlite3
import random


def get_yml_data():
    """Function that open a yaml file and get the necessary information."""
    try:
        with open('config.yml', 'r') as fr:
            data = yaml.safe_load(fr)
            return data
    except OSError():
        sys.exit(2)


data_config = get_yml_data()
URL = data_config.get('url')
API_KEY = data_config.get('api_key')
ingred = data_config.get('ingredient')


class Generator:
    def __init__(self, ingredients):
        """Set the parameter that will be used in the process to get data."""
        self.ingredients = ingredients
        self.url = URL
        self.api = API_KEY

    def _get_recipe(self):
        """It converted the information coming from the API and returns it as json result."""
        response = requests.get(self.url, params=self._param()).json()
        return response

    def _param(self):
        """Sets the endpoint of the request."""
        take = self.ingredients
        return {'ingredients': take, 'apiKey': self.api}

    def get_data_from_web(self):
        """Append the main recipe information to a list."""
        list_of_result = []
        responsee = self._get_recipe()
        for item in responsee:
            finally_data = {'id': item['id'], 'title': item['title'], 'image': item['image']}
            list_of_result.append(finally_data)
        return list_of_result

    def sql_db(self):
        """Created a sql database with information coming from another function as input."""
        con = sqlite3.connect('Generator.db')
        cursor = con.cursor()
        create_command = '''CREATE TABLE IF NOT EXISTS Generator(
                id INTEGER PRIMARY KEY,
                title TEXT(20),
                image TEXT(20));
               '''
        cursor.execute(create_command)
        insert = self.get_data_from_web()
        # return the list
        info = []
        for item in insert:
            info.append(item['id'])
        r = random.choice(info)
        cursor.execute('SELECT * FROM Generator WHERE id = ?;', (r, ))
        c = cursor.fetchall()
        print(c)
        # Add info to the database
        for itemm in insert:
            cursor.execute('INSERT INTO Generator VALUES (:id, :title, :image)', itemm)
            con.commit()
        con.close()


if __name__ == '__main__':
    ingredient = input('Insert here: ')
    app = Generator(ingredient)
    app.sql_db()
