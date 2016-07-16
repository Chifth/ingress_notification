# Ingress Attack Notifier

## Run it by docker-compose

- Install `docker` & `docker-compose`
  - https://docs.docker.com/engine/installation/
  - https://docs.docker.com/compose/install/
- Edit `docker-compose.yml`
  - Replace `<your_username>` / `<your_password>` / `<your_telegram_bot_token>`.
- Run
  - `docker-compose up [-d]`

## Run it manually

- Install dependencies
  - `pip install -r requirements.txt`
- Run
  - `USERNAME=<your_username> PASSWORD=<your_password> TELEGRAM_TOKEN=<your_telegram_bot_token> PYTHONIOENCODING=utf-8 ./main.py`
