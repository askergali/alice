import requests
from random import sample, shuffle, randint
from flask import Flask, request
import logging
import json


class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.book = None

    def is_logged(self):

        if self.name is not None:
            return True
        else:
            return False

    def get_name(self):
        return self.name

    def set_book(self, book):
        self.book = book

    def get_book(self):
        return self.book


class Book:
    def __init__(self, title, rating, desc, cover):
        self.title = title
        self.rating = rating
        # self.author = author
        self.desc = desc
        self.cover = cover

    def get_cover(self):
        return self.cover


user = None

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
sessionStorage = {}


def get_rating(book_name):
    try:
        url = "https://www.googleapis.com/books/v1/volumes"

        params = {
            'q': book_name,
            'key': "AIzaSyASRytsKdbn784sNbZz5yqJVySiWuSUIik"
        }

        response = requests.get(url, params=params)
        books_json = response.json()

        rating = books_json['items'][0]['volumeInfo']['averageRating']
        name_book = books_json['items'][0]['volumeInfo']['title']

        return rating, name_book

    except Exception as e:
        return e


def get_description(book_name):
    try:
        url = "https://www.googleapis.com/books/v1/volumes"

        params = {
            'q': book_name,
            'key': "AIzaSyASRytsKdbn784sNbZz5yqJVySiWuSUIik"
        }

        response = requests.get(url, params=params)
        books_json = response.json()

        description = books_json['items'][0]['volumeInfo']['description']

        return description

    except Exception as e:
        return e


def get_cover(book_name='harry potter and chamber of secrets'):
    try:
        url = "https://www.googleapis.com/books/v1/volumes"

        params = {
            'q': book_name,
            'key': "AIzaSyASRytsKdbn784sNbZz5yqJVySiWuSUIik"
        }

        response = requests.get(url, params=params)
        books_json = response.json()

        cover = books_json['items'][0]['volumeInfo']['imageLinks']['thumbnail']

        return cover

    except Exception as e:
        return e


def get_first_name(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            return entity['value'].get('first_name', None)


books = []
authors = []
author_book = {}

book_4authors = []
new_b4a = []


def get_books():
    try:

        response = requests.get(
            "https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?api-key=03GX5gN25mrINUZTbJV5Y4cXKPYU8f49")
        books_json = response.json()
        for i in range(20):
            book = books_json['results'][i]['title']
            books.append(book)

    except Exception as e:
        return e

    return books


def get_authors():
    try:

        response = requests.get(
            "https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?api-key=03GX5gN25mrINUZTbJV5Y4cXKPYU8f49")
        books_json = response.json()
        for i in range(20):
            author = books_json['results'][i]['author']
            authors.append(author)

    except Exception as e:
        return e

    return authors


def get_book_and_author():
    try:

        response = requests.get(
            "https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?api-key=03GX5gN25mrINUZTbJV5Y4cXKPYU8f49")
        books_json = response.json()
        for i in range(20):
            author_book[books_json['results'][i]['title']] = books_json['results'][i]['author']

    except Exception as e:
        return e

    return author_book


def guess_author():
    book = random_book()[0]

    shuffle(authors)

    for i in range(3):
        book_4authors.append(authors[i])

    book_4authors.append(author_book[book])

    return book, book_4authors


def new_list_of_authors():
    new_b4a = sample(book_4authors, len(book_4authors))
    return new_b4a


def random_book():
    shuffle(books)
    return books[0], author_book[books[0]]


get_books()
get_authors()
get_book_and_author()

genres = ['Fiction', 'Action', 'Classic', 'Comic', 'Detective', 'Drama', 'Horror']
book_names = ['Harry Potter', 'The Hobbit', '1984', 'Batman', 'Sherlock Holmes', 'Hamlet', 'The Shining']

books_4genres = {
    'Harry Potter': 'Fiction',
    'The Hobbit': 'Action',
    '1984': 'Classic',
    'Batman': 'Comic',
    'Sherlock Holmes': 'Detective',
    'Hamlet': 'Drama',
    'The Shining': 'Horror'
}


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    global user

    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Это навык Книги. Представься, пожалуйста'
        sessionStorage[user_id] = {
            'first_name': None,
            'prev_answer': ""
        }

        return

    if user is None:
        user = User(user_id, get_first_name(req))
        if user.get_name() is None:
            res['response']['text'] = 'Не расслышала имя. Повтори, пожалуйста'
        else:
            # sessionStorage[user_id]['first_name'] = first_name
            user = User(user_id, get_first_name(req))
            res['response']['text'] = 'Приятно познакомиться, ' + user.get_name().title() \
                                      + '. Я - Алиса. Я могу порекомендовать тебе книгу, дать рецензию на уже интересующую ' \
                                        'или проверить твои знания в литературе!'
            res['response']['buttons'] = [
                {
                    'title': 'Рекомендация',
                    'hide': True
                },
                {
                    'title': 'Рецензия',
                    'hide': True
                },
                {
                    'title': 'Тест',
                    'hide': True
                }
            ]
    else:
        if 'рекомендация' in req['request']['nlu']['tokens']:
            book, author = random_book()
            res['response']['text'] = 'Советую почитать ' + book + ' от автора ' + author + ', ' + user.get_name().title()

        elif 'тест' in req['request']['nlu']['tokens']:
            res['response']['text'] = 'Ты решил пройти тест! По авторам или по жанрам?'

            res['response']['buttons'] = [
                {
                    'title': 'По авторам',
                    'hide': True
                },
                {
                    'title': 'По жанрам',
                    'hide': True
                }
            ]

            sessionStorage[user_id]['prev_answer'] = 'Тест'

        elif sessionStorage[user_id]['prev_answer'] == 'Тест':
            sessionStorage[user_id]['prev_answer'] = ""

            if req['request']['command'] == 'По авторам':

                name, authors = guess_author()
                new_authors = new_list_of_authors()

                res['response']['text'] = 'Назовите автора этой книги:' + '\n' + name

                res['response']['buttons'] = [
                    {
                        'title': new_authors[0],
                        'hide': True
                    },
                    {
                        'title': new_authors[1],
                        'hide': True
                    },
                    {
                        'title': new_authors[2],
                        'hide': True
                    },
                    {
                        'title': new_authors[3],
                        'hide': True
                    }
                ]

                if req['request']['command'] == authors[-1]:
                    sessionStorage[user_id]['prev_answer'] = 'verno'

                else:
                    sessionStorage[user_id]['prev_answer'] = 'neverno'

            elif req['request']['command'] == 'По жанрам':
                book_genre = book_names[randint(0, 7)]
                res['response']['text'] = 'Назовите жанр этой книги:' + '\n' + book_genre

                if req['request']['command'] == books_4genres[book_genre]:
                    sessionStorage[user_id]['prev_answer'] = 'verno'

                else:
                    sessionStorage[user_id]['prev_answer'] = 'neverno'

            else:
                res['response']['text'] = 'Не вредничай'
                res['response']['buttons'] = [
                    {
                        'title': 'По авторам',
                        'hide': True
                    },
                    {
                        'title': 'По жанрам',
                        'hide': True
                    }
                ]

        elif sessionStorage[user_id]['prev_answer'] == 'verno':

            sessionStorage[user_id]['prev_answer'] = ''
            res['response']['text'] = 'Правильно'

        elif sessionStorage[user_id]['prev_answer'] == 'neverno':

            sessionStorage[user_id]['prev_answer'] = ''
            res['response']['text'] = 'Не расстраивайся'

        elif 'рецензия' in req['request']['nlu']['tokens']:
            res['response']['text'] = 'Напиши название книги (на английском языке)'
            # sessionStorage[user_id]['prev_answer'] = 'Напиши название книги (на английском языке)'
        elif user.get_book() is None:
            # sessionStorage[user_id]['prev_answer'] = ""
            book_name = req['request']['command']

            rating, name_book = get_rating(book_name)
            description = get_description(book_name)
            cover = get_cover(book_name)

            book = Book(title=name_book, rating=rating, desc=description, cover=cover)

            user.set_book(book)

            res['response']['text'] = name_book + ':' + '\n' + 'Рейтинг - ' + str(
                rating) + '\n' + 'Описание - ' + description + '\n' + 'Хотите увидеть обложку?'
            res['response']['buttons'] = [
                {
                    'title': 'Да',
                    'hide': True
                },
                {
                    'title': 'Нет',
                    'hide': True
                }
            ]
        elif user.get_book():
            if 'да' in req['request']['nlu']['tokens']:
                res['response']['text'] = 'Нажми на ссылку чтобы увидеть обложку'
                res['response']['buttons'] = [
                    {
                        'title': 'Обложка',
                        'url': user.get_book().get_cover(),
                        'hide': True
                    }
                ]

            else:
                res['response']['text'] = 'Что-то еще?'
                res['response']['buttons'] = [
                    {
                        'title': 'Рекомендация',
                        'hide': True
                    },
                    {
                        'title': 'Рецензия',
                        'hide': True
                    },
                    {
                        'title': 'Тест',
                        'hide': True
                    }
                ]
            user.set_book(None)
        elif 'обложка' in req['request']['nlu']['tokens']:
            res['response']['text'] = 'Что-то еще?'
            res['response']['buttons'] = [
                {
                    'title': 'Рекомендация',
                    'hide': True
                },
                {
                    'title': 'Рецензия',
                    'hide': True
                },
                {
                    'title': 'Тест',
                    'hide': True
                }
            ]
        else:
            res['response']['text'] = 'Ты должен выбрать!'
            res['response']['buttons'] = [
                {
                    'title': 'Рекомендация',
                    'hide': True
                },
                {
                    'title': 'Рецензия',
                    'hide': True
                },
                {
                    'title': 'Тест',
                    'hide': True
                }
            ]


if __name__ == '__main__':
    app.run()
