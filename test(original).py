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

    def startedQuizGenre(self, quizGenre):
        self.quizGenre = quizGenre
        self.isTakingQuizGenre = True

    def startedQuizAuthor(self, quizAuthor):
        self.quizAuthor = quizAuthor
        self.isTakingQuizAuthor = True

    def get_name(self):
        return self.name

    def set_book(self, book):
        self.book = book

    def get_book(self):
        return self.book


class QuizGenre:
    def __init__(self, questions, answers):
        self.questions = questions
        self.answers = answers
        self.currentQuestion = 0
        self.totalScore = 0

    def get_quizGenre(self):
        global genres
        book = self.questions[self.currentQuestion]
        genre = self.answers[self.currentQuestion]
        options = []
        while len(options) <= 3:
            option = genres[randint(0, len(genres))]
            if option != genre:
                options.append(option)

        options.append(genre)
        shuffled_genres = shuffle(options)
        return book, genre, shuffled_genres

    def randomBook_and_Genre(self):
        global book_names, books_4genres

        randomBooks_g = []
        correctGenres = []
        book_g = book_names[randint(0, len(book_names))]
        correctGenre = books_4genres[book_g]
        randomBooks_g.append(book_g)
        correctGenres.append(correctGenre)
        return randomBooks_g, correctGenres

    def answer(self, answer):
        if answer == self.answers[self.currentQuestion]:
            self.totalScore += 1
            self.currentQuestion += 1
        else:
            self.currentQuestion += 1

    def end_quiz(self):
        if self.currentQuestion == 5:
            user.isTakingQuizGenre = False


class QuizAuthor:
    def __init__(self, questions, answers):
        self.questions = questions
        self.answers = answers
        self.currentQuestion = 0
        self.totalScore = 0

    def get_quizAuthor(self):
        global all_authors
        book = self.questions[self.currentQuestion]
        author = self.answers[self.currentQuestion]
        choices = []
        while len(choices) <= 3:
            choice = all_authors[randint(0, len(all_authors))]
            if choice != author:
                choices.append(choice)

        choices.append(author)
        shuffled_authors = shuffle(choices)
        return book, author, shuffled_authors

    def randomBooks_and_Authors(self):
        randomBooks = []
        correctAnswers = []
        book, author = random_book()
        randomBooks.append(book)
        correctAnswers.append(author)
        return randomBooks, correctAnswers

    def answer(self, answer):
        if answer == self.answers[self.currentQuestion]:
            self.totalScore += 1
            self.currentQuestion += 1
        else:
            self.currentQuestion += 1

    def end_quiz(self):
        user.isTakingQuizAuthor = False


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

        author = books_json['items'][0]['volumeInfo']['authors'][0]
        description = books_json['items'][0]['volumeInfo']['description']

        return author, description

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


def get_book_and_author():
    global all_books, all_authors, author_book
    try:

        response = requests.get(
            "https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?api-key=03GX5gN25mrINUZTbJV5Y4cXKPYU8f49")
        books_json = response.json()
        for i in range(20):
            book = books_json['results'][i]['title']
            all_books.append(book)

            author = books_json['results'][i]['author']
            all_authors.append(author)

            author_book[book] = author

    except Exception as e:
        return e

    return all_books, all_authors, author_book


def random_book():
    global all_books
    shuffle(all_books)
    return all_books[0], author_book[all_books[0]]

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
            user = User(user_id, get_first_name(req))
            res['response']['text'] = 'Приятно познакомиться, ' + user.get_name().title() \
                                      + '. Я - Алиса. Я могу порекомендовать тебе книгу, дать рецензию на уже ' \
                                        'интересующую или проверить твои знания в литературе!'
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
                res['response']['text'] = 'po avtoram'

            elif req['request']['command'] == 'По жанрам':
                res['response']['text'] = 'no zhanram'

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

        elif 'рецензия' in req['request']['nlu']['tokens']:
            res['response']['text'] = 'Напиши название книги (на английском языке)'

        elif user.get_book() is None:
            book_name = req['request']['command']

            rating, name_book = get_rating(book_name)
            author_name_book, description = get_description(book_name)
            cover = get_cover(book_name)

            book = Book(title=name_book, rating=rating, author=author_name_book, desc=description, cover=cover)

            user.set_book(book)

            res['response']['text'] = name_book + ':' + '\n' + 'Автор - ' + author_name_book + '\n' + 'Рейтинг - ' + str(
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
                res['response']['text'] = 'Перейди по ссылке чтоб посмотреть на обложку'
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
