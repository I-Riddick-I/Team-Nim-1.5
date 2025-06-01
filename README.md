# Team-Nim-1.5
## Start

1. #### Virtual environment

    1. #### Create virtual environment (**venv**)
        ```
        python -m venv [path to venv folder]
        ```

    2. #### Activate **venv**
        ```
        [path to venv folder]\Scripts\activate
        ```

2. #### Install **requirements**
    ```
    pip install -r requirements.txt
    ```

 3. #### Configure
 
    Get Telegram **bot token** via https://t.me/BotFather and use:
    ```
    python -m main.configure
    ```

4. #### Run
    ```
    python -m main.run
    ```

---

## Setup

1. See `AuthCode: [code]` in terminal  and use command `/auth [code]` in private chat with bot

   * if you know your telegram id: before running bot open `configs/config.json` and in list with key `"ADMINS"` add telegram ids of users that should have rights to control bot. \
   Also you can set chat id in `"ADMINS_CHAT"` where bot should send notices about violations or use command `/setAdminsChat` in the desired chat
