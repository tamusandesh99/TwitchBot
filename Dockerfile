FROM python:3.8
WORKDIR /TwitchBot
COPY requirements.txt /TwitchBot/
RUN pip3 install -r requirements.txt
COPY . /TwitchBot
CMD python3 bot.py
