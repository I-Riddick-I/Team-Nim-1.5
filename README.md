# Team-Nim-1.5

## Start

1. ### Virtual environment

    1. Create virtual environment (**venv**)

        ```[]
        python -m venv [path to venv folder]
        ```

    2. Activate **venv**

        ```[]
        [path to venv folder]\Scripts\activate
        ```

2. ### Install **requirements**

    ```[]
    pip install -r requirements.txt
    ```

3. ### Configure

    Get Telegram **bot token** via <https://t.me/BotFather> and use:

    ```[]
    python -m main.configure
    ```

4. ### Run

    ```[]
    python -m main.run
    ```

---

## Setup

1. After running see `AuthCode: [code]` in terminal  and use command `/auth [code]` in private chat with bot

    > if you know your telegram id: before running bot open `configs/config.json` and in list with key `"ADMINS"` add telegram ids of users that should have rights to control bot. \
    Also you can set chat id in `"ADMINS_CHAT"` where bot should send notices about violations or use command `/setAdminsChat` in the desired chat

2. Add bot to group

3. Give to bot admin rights
    > Bot must have these rights:
    * Delete messages
    * Block users

4. Make sure that group migrate to **supergroup**

    > You can check this by command `/info`

5. Use command `/addGroup`

---

## Commands list

* ### auth [code]

  > Используется единожды для авторизации. \
  > В случае успешного ввода кода, id пользователя добавляется в список администраторов.

Все дальнейшие команды доступны только для админов.

* ### info

  > Краткая информация о текущем чате.

* ### setAdminsChat

  > Позволяет выбрать чат для оповещений. \
  > Используйте эту команду в нужном чате. \
  > Чтобы поменять чат просто используйте эту команду в нужном чате.

* ### delAdminsChat

  > Удаляет данные о чате для оповещений. \
  > Можно использовать в любом чате.

* ### addGroup

  > Добавляет id текущей группы в список разрешённых групп.

* ### removeGroup

  > Удаляет id текущей группы из списка разрешённых групп.

* ### addAdmin

  > Добавляет пользователя в список администраторов

* ### removeAdmin

  > Удаляет пользователя из списка администраторов

* ### myId

  > Возвращает id пользователя.

* ### chatId

  > Возвращает id чата.

* ### messageId

  > Возвращает id пересланного сообщения. \
  > Если пересланное сообщение отсутствует, возвращает id сообщения команды.

* ### userId

  > Возвращает id отправителя пересланного сообщения.

* ### adminsList

  > Возвращает список пользовательских имён админов

---
