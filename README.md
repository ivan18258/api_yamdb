# Групповой проект - "YaMDb"

## Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Пользовательские роли и права доступа

- Аноним — может просматривать описания произведений, читать отзывы и комментарии.

- Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.

- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.

- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

- Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

## Аутентификация
Используется аутентификация с использованием JWT-токенов

## Установка
Клонировать репозиторий и перейти в него в командной строке:

> https://github.com/ivan18258/api_yamdb.git

> cd api_yamdb

Cоздать и активировать виртуальное окружение:

> python -m venv venv

> source venv/Scripts/activate

> python -m pip install --upgrade pip

Установить зависимости из файла requirements.txt:

> pip install -r requirements.txt

Выполнить миграции:

> python manage.py migrate

Запустить проект:

> python manage.py runserver

## Примеры запросов к API:

Метод запроса: POST  
URL-адрес запроса: http://127.0.0.1:8000/api/v1/titles/

### Тестовые данные

В проекте есть тестовые данные, загружаемые manage командой

pythоn manage.py load_test_base