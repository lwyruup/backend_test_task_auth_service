# Тестовое задание Junior Backend разработчик

Сервис аутентификации и авторизации с поддержкой контроля доступа.





## Стек

- Python 3.9
- Django+DRF
- drf-spectacular (Swagger)
- PostgreSQL 


---

## Установка

```bash
git clone <repo>
cd auth_system
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

## Запуск

Создайте базу в PostgreSQL
```bash
createdb auth_system_db
```
Примените миграции
```bash
python manage.py migrate
```
Загрузите фикстуры
```bash
python manage.py loaddata fixtures/initial_data.json
```
Запустите сервер
```bash
python manage.py runserver
```
Создание суперпользователя(опционально)
```bash
python manage.py createsuperuser
```


Готовые пользователи:
1. email: adminik@example.com, пароль: admin123(superuser)
2. email: test@example.com, пароль: 12345678(admin)
3. email: test2@example.com, пароль: 12345678
4. email: second@example.com, пароль: second123
5. email: third@example.com, пароль: third123


## API документация
SWAGGER: **http://127.0.0.1:8000/api/docs/**

## Аутентификация
- Аутентификация основана на токенах сессии
- Для авторизации нужно ввести токен в заголовок: Authorization: Bearer <access_token>


## Некоторые эндпоинты

Примеры curl:
- Регистрация
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"12345678","first_name":"Test"}'
```
- Логин
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"12345678"}'
```
- Получение пользователя по токену:
```bash
curl http://127.0.0.1:8000/api/auth/me/ \
  -H "Authorization: Bearer <TOKEN>"
```

## Как работает система контроля доступа?

Система ограничений доступа реализована на основе трёх сущностей:

---

1. Роли

Опредеяет роль пользователя(admin, user, manager и тд.). У каждой роли есть id, имя и описание.


Таблица: roles.
Модель: Role


Каждый пользователь связан с одной ролью.



2. Бизнес-элементы

Это специальные объекты системы, к которым нужно регулировать доступ:

Например:
- Элемент users — операции над пользователями
- Элемент roles — операции над ролями

Таблица: business_elements.
Модель: BusinessElement

У бизнес-элемента есть поля id, code(уникальный код для каждого элемента), name



3. Правила доступа

Правила определяют, что конкретная роль может делать с конкретным бизнес-элементом.

Таблица: access_role_rules
Модель: AccessRule

Поля:
    role_id ---> FK на Role,
	element_id ---> FK на BusinessElement

И  есть набор флагов(доступ к разным операциям):
	read_permission,
	read_all_permission,
	create_permission,
	update_permission,
	update_all_permission,
	delete_permission,
	delete_all_permission,

Как взаимодействуют сущности между собой:
1. У пользователя есть роль. Для этой роли в Правилах доступа(access_rules) заданы разрешения.
И каждая роль имеет свои правила доступа к конкретному бизнес-элементу. Например, пользователь с ролью admin имеет все разрешения на все бизнес-елементы(в нашем случае на элементы users, roles), пользовател  user не имеет разрешений ни к какому элементу и тд.
2. Каждый эндпоинт в API, связанный с контролем доступа имеет методы сrud
3. Текущий пользователь определятеся по токену. Если токена нет или он истек, то возвращается 401 статус.
4. После определения пользователя находится бизнес-элемент по коду, далее находится само правило доступа. Если правила нет, то возвращается 403 статус.
5. Последним шагом проверяется, имеет ли пользователь с данной ролью разрешение(через флаги). Если не имеет - возвращается 403 статус.

