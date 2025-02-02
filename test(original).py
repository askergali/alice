import requests
from random import sample, shuffle, randint
from flask import Flask, request
import logging
import json


def randomBooks_and_Authors():
    questions_authors, answers_authors = [], []
    for i in range(5):
        book, author = random_book()
        questions_authors.append(book)
        answers_authors.append(author)
    return questions_authors, answers_authors


def randomBook_and_Genre():
    global book_names, books_4genres

    questions_genres, answers_genres = [], []
    for i in range(5):
        book_g = book_names[randint(0, len(book_names)-1)]
        correctGenre = books_4genres[book_g]
        questions_genres.append(book_g)
        answers_genres.append(correctGenre)
    return questions_genres, answers_genres


class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.book = None
        self.isTakingQuizGenre = False
        self.quizGenre = None
        self.isTakingQuizAuthor = False
        self.quizAuthor = None

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

    def get_quizAuthor(self):
        return self.quizAuthor

    def get_quizGenre(self):
        return self.quizGenre

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

    def quizGenre(self):
        global genres
        book = self.questions[self.currentQuestion-1]
        genre = self.answers[self.currentQuestion-1]
        options = []
        while len(options) <= 2:
            option = genres[randint(0, len(genres)-1)]
            if option != genre:
                options.append(option)

        options.append(genre)
        shuffled_genres = sample(options, len(options))
        return book, genre, shuffled_genres

    def answer(self, answer):
        if answer == self.answers[self.currentQuestion-1]:
            self.totalScore += 1
            self.currentQuestion += 1
        else:
            self.currentQuestion += 1
        return self.currentQuestion, self.totalScore

    def end_quiz(self):
        user.isTakingQuizGenre = False


class QuizAuthor:
    def __init__(self, questions, answers):
        self.questions = questions
        self.answers = answers
        self.currentQuestion = 0
        self.totalScore = 0

    def quizAuthor(self):
        global all_authors
        book = self.questions[self.currentQuestion-1]
        author = self.answers[self.currentQuestion-1]
        choices = []
        while len(choices) <= 2:
            choice = all_authors[randint(0, len(all_authors)-1)]
            if choice != author:
                choices.append(choice)

        choices.append(author)
        shuffled_authors = sample(choices, len(choices))
        return book, author, shuffled_authors

    def answer(self, answer):
        if answer == self.answers[self.currentQuestion-1]:
            self.totalScore += 1
        self.currentQuestion += 1
        return self.currentQuestion, self.totalScore

    def end_quiz(self):
        user.isTakingQuizAuthor = False


class Book:
    def __init__(self, title, rating, author, desc, cover):
        self.title = title
        self.rating = rating
        self.author = author
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
        return None, e


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
        return e, None


def get_cover(book_name):
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

    except Exception:
        return None


def get_first_name(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            return entity['value'].get('first_name', None)


all_books = []
all_authors = []
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
                },
                {
                    'title': 'Google Books API',
                    'url': 'https://developers.google.com/books/docs/overview',
                    'hide': True
                },
                {
                    'title': 'New York Times API',
                    'url': 'https://developer.nytimes.com/docs/books-product/1/overview',
                    'hide': True
                }
            ]
    else:
        if 'рекомендация' in req['request']['nlu']['tokens']:
            book, author = random_book()
            res['response']['text'] = 'Советую почитать ' + book + ' от автора ' + author + ', ' + user.get_name().title()
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
        elif 'авторам' in req['request']['nlu']['tokens']:
            questions_authors, answers_authors = randomBooks_and_Authors()
            quiz_author = QuizAuthor(questions=questions_authors, answers=answers_authors)
            user.startedQuizAuthor(quizAuthor=quiz_author)
            user.isTakingQuizAuthor = True
            book_author, author_author, varianti = user.quizAuthor.quizAuthor()
            res['response']['text'] = 'Назовите автора данной книги: ' + '\n' + book_author
            res['response']['buttons'] = [
                {
                    'title': varianti[0],
                    'hide': True
                },
                {
                    'title': varianti[1],
                    'hide': True
                },
                {
                    'title': varianti[2],
                    'hide': True
                },
                {
                    'title': varianti[3],
                    'hide': True
                }
            ]
        elif user.isTakingQuizAuthor:
            answer = req['request']['command']
            current, total = user.quizAuthor.answer(answer=answer)
            book_author, author_author, varianti = user.quizAuthor.quizAuthor()
            if current < 5:
                res['response']['text'] = 'Ваш нынешний результат: ' + str(total) + '/5' + '\n' + 'Назовите автора данной книги: ' + '\n' + book_author
                res['response']['buttons'] = [
                    {
                        'title': varianti[0],
                        'hide': True
                    },
                    {
                        'title': varianti[1],
                        'hide': True
                    },
                    {
                        'title': varianti[2],
                        'hide': True
                    },
                    {
                        'title': varianti[3],
                        'hide': True
                    }
                ]
            else:
                res['response']['text'] = 'Вы прошли тест на литературные знания.' + '\n' + 'Ваш результат: ' + str(total) + '/5'
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
                user.isTakingQuizAuthor = False
        elif 'жанрам' in req['request']['nlu']['tokens']:
            questions_genres, answers_genres = randomBook_and_Genre()
            quiz_genre = QuizGenre(questions=questions_genres, answers=answers_genres)
            user.startedQuizGenre(quizGenre=quiz_genre)
            user.isTakingQuizGenre = True
            book_genre, genre_genre, varianti_genre = user.quizGenre.quizGenre()
            res['response']['text'] = 'Назовите жанр данной книги: ' + '\n' + book_genre
            res['response']['buttons'] = [
                {
                    'title': varianti_genre[0],
                    'hide': True
                },
                {
                    'title': varianti_genre[1],
                    'hide': True
                },
                {
                    'title': varianti_genre[2],
                    'hide': True
                },
                {
                    'title': varianti_genre[3],
                    'hide': True
                }
            ]
        elif user.isTakingQuizGenre:
            answer_genre = req['request']['command']
            current_g, total_g = user.quizGenre.answer(answer=answer_genre)
            book_genre, genre_genre, varianti_genre = user.quizGenre.quizGenre()
            if current_g < 5:
                res['response']['text'] = 'Ваш нынешний результат: ' + str(total_g) + '/5' + '\n' + 'Назовите жанр данной книги: ' + '\n' + book_genre
                res['response']['buttons'] = [
                    {
                        'title': varianti_genre[0],
                        'hide': True
                    },
                    {
                        'title': varianti_genre[1],
                        'hide': True
                    },
                    {
                        'title': varianti_genre[2],
                        'hide': True
                    },
                    {
                        'title': varianti_genre[3],
                        'hide': True
                    }
                ]
            else:
                res['response']['text'] = 'Вы прошли тест на литературные знания.' + '\n' + 'Ваш результат: ' + str(total_g) + '/5'
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
                user.isTakingQuizGenre = False
        elif 'рецензия' in req['request']['nlu']['tokens']:
            res['response']['text'] = 'Напиши название книги (на английском языке)'
        elif 'api' in req['request']['nlu']['tokens']:
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
        elif user.get_book() is None:
            book_name = req['request']['command']

            rating, name_book = get_rating(book_name)
            if rating is None:
                res['response']['text'] = 'Недостаточно данных'
                return
            author_name_book, description = get_description(book_name)
            if description is None:
                res['response']['text'] = 'Недостаточно данных'
                return
            cover = get_cover(book_name)
            if cover is None:
                res['response']['text'] = 'Недостаточно данных'
                return

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
    app.run(port=31373)
