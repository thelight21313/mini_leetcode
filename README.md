# Mini Leetcode

Платформа для онлайн-соревнований по программированию.

## О проекте

**Mini Leetcode** — пет-проект, представляющий собой мини-аналог LeetCode. Платформа позволяет пользователям решать алгоритмические задачи, участвовать в контестах и получать мгновенную обратную связь о результатах проверки кода.

Код запускается в изолированной среде через **Judge0**, проверяется на всех тест-кейсах, а результат доставляется пользователю в реальном времени через **WebSocket**.

---

## Стек технологий

### Бэкенд

* **Django + Django REST Framework** — основной фреймворк и API
* **PostgreSQL** — основная база данных
* **Celery** — фоновая проверка решений
* **Redis** — брокер задач Celery и кэш
* **Django Channels** — WebSocket для realtime-уведомлений
* **Judge0** — изолированный сервис запуска кода
* **JWT-авторизация** через SimpleJWT
* **dj-rest-auth + django-allauth** — регистрация и аутентификация

### Инфраструктура

* **Docker + Docker Compose** — контейнеризация всех сервисов
* **Nginx** — проксирование **HTTPS/WebSocket** и раздача статики
* **Daphne** — ASGI сервер

### Фронтенд

* **Чистый HTML + Vanilla JS**, без фреймворков
* **Monaco Editor (CDN)** — редактор кода в браузере
* JWT хранится в `localStorage`

---

## Архитектура

Проект разбит на несколько Django-приложений:

* `users` — кастомная модель пользователя (`AbstractUser`)
* `problems` — задачи, теги, тест-кейсы
* `submissions` — отправки решений, проверки, WebSocket на статус
* `contests` — соревнования (задачи видны только участникам, после завершения становятся публичными, лидерборд хранится в Redis)

---

## Процесс проверки решения

1. Пользователь отправляет код через `POST /api/submissions/`
2. Создаётся запись `Submission` со статусом `pending`
3. Запускается Celery-задача `check_submission`
4. Задача последовательно прогоняет код через все тест-кейсы задачи, отправляя каждый в Judge0
5. При каждом изменении статуса (`running → accepted / wrong_answer / ...`) уведомление отправляется через Django Channels
6. Фронтенд подключается по WebSocket `wss://.../ws/submissions/<id>/` и отображает результат в реальном времени

---

## Основные API-эндпоинты

* `GET /api/problems/` — список задач с фильтрацией по сложности, тегам, поиску и пагинацией
* `GET /api/problems/<slug>/` — детальная страница задачи с примерами и последним кодом пользователя
* `GET /api/tags/` — список тегов
* `POST /api/submissions/` — отправить решение
* `GET /api/submissions/<id>/` — статус решения
* `POST /api/token/` — получить JWT по `username/password`
* `POST /api/auth/registration/` — регистрация

---

## Как запустить

```bash
git clone https://github.com/thelight21313/mini_leetcode
cd mini-leetcode

docker compose up -d --build
docker compose exec django-app python manage.py migrate
```

### HTTPS / Nginx

Nginx уже настроен для работы по **HTTPS**, включая поддержку **WebSocket Secure (`wss://`)**.

Если используются свои сертификаты, убедитесь, что пути к `fullchain.pem` и `privkey.pem` корректно указаны в конфигурации Nginx или подключены через Docker volumes.
