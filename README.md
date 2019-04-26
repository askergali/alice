# Alice's skill - Books

## Описание навыка
Навык для Яндекс Алисы, разработанный для работы с книгами при использовании сторонних API. 

## Описание работы навыка
Навык запрашивает имя пользователя и предлагает ему на выбор три опции - Рекомендация, Рецензия или Тест, выполняемые сколько угодно раз.

## Подробнее о возможностях навыка
```
1) О функции Рекомендация: возращает рандомную книгу и ее автор. Осуществляется при помощи New York Times Books API.
2) О функции Рецензия: возвращает правильное название, автора, средний рейтинг, описание и, по желанию, обложку интересующей пользователя книги. Осуществляется при помощи Google Books API.
3) О функции Тест: на выбор пользователя начинается тест по авторам или по жанрам. Всего в тесте 5 вопросов с четырьмя вариантами ответов. Осуществляется при помощи New York Times Books API.
```

## Библиотеки и работа с API
1) Используются библиотеки requests, random, flask, logging и json.
2) Два API: New York Times Books API и Google Books API.

New York Times Books API: [link to documentation](https://developer.nytimes.com/docs/book-product/1/overview)

Google Books API: [link to documentation](https://developers.google.com/books/docs/overview)


## Классы
В данном навыке используется 4 класса: классы User, Book, QuizGenre и QuizAuthor. 

## Автор проекта
**Askergali Aigerim** - [askergali](https://github.com/askergali)
