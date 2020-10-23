all: run

clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist #&& rm -rf *.log*

venv:
	virtualenv --python=python3 venv && venv/bin/pip install -r requirements

run: venv
	venv/bin/python bot.py

test: venv
	venv/bin/python -m unittest discover -s tests

docker-build:
	docker build -t discord-bot .

docker-run:	docker-build
	-docker stop discord-bot
	-docker rm discord-bot
	docker run -d --restart=always -v /path/to/memes:/app/memes -v /path/to/logs/discord.log:/app/discord.log --name discord-bot discord-bot

docker-stop:
	docker stop discord-bot