FROM python:3.8

RUN pip install discord.py==1.5.0

COPY ./ /app
WORKDIR /app

CMD ["python", "-u", "bot.py"]
#               -u to get print statement to container logs
