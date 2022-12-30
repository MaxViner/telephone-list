@echo_off

call %~dp0GicBrains\venv\Scripts\activate

cd %~dp0GicBrains

set TOKEN=5974704275:AAENn0SnIZ4iHQj-jdNDbQjoJ5bnFfTSsc8

python tgBot.py

pauser