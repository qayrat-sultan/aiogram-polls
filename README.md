### [![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)  [![Aiogram](https://img.shields.io/badge/aiogram-2.18-blue)](https://pypi.org/project/aiogram/) 

### About
Scalable and straightforward template for bots written on [aiogram](https://github.com/aiogram/aiogram).

### Setting up

#### System dependencies
- Python 3.8+
- GNU/Make 
- GIT

#### Preparations
- Clone this repo via `git clone https://github.com/qayrat-sultan/aiogram-template`;
- Move to the directory `cd aiogram-template`.

#### Virtualenv deployment
- **Note:** You need to have Virtualenv installed.;
- Create virtual environment dir: `virtualenv venv` or `python -m venv venv`;
- Activate your virtualenv: Unix: `source venv/bin/activate` or Win: `venv\Scripts\activate`
- Rename `dist.env` to `.env` and replace a token placeholder with your own one;
- Install requirement libraries: `pip install -r req.txt`
- If use MongoDB server:
-  1. `pip install pymongo[srv]`
-  2. Visit mongodb.com and create cluster
-  3. Copy host url string and paste .env MONGO_URL variable
- Start the bot: `python bot.py`.

**Tip**: set `BOT_TOKEN` environment variable to change bot token. If no variable is specified, it'll not working.
