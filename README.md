# Дипломный проект Яндекс Практикум

# Foodgram - сервис для размещения кулинарных рецептов с возможностью подписки на автора.

Онлайн-сервис, в котором пользователи могут публиковать свои рецепты, добавлять рецепты в избранное и подписываться на других авторов, скачивать список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Проект развернут на сервере: [kommgramm.ddns.net](https://kommgramm.ddns.net/)

## Суперпользователь для проверки: info@mail.ru foodgram123

### Для запуска проекта в контейнерах выполните команду:
```
sudo docker compose up -d --build
```
### Выполните миграции, создайте суперпользователя и соберите статику
```
sudo docker compose exec backend python manage.py migrate
sudo docker compose exec backend python manage.py createsuperuser
sudo docker compose exec backend python manage.py collectstatic --no-input 
```
### Ресурсы проекта:
* http://localhost/ - главная страница сайта;
* http://localhost/admin/ - админ панель;
* http://localhost/api/ - API проекта
* http://localhost/api/docs/redoc.html - документация к API

### Автор:
#### Михаил Комиссаров
