# discord-alma-bot
ALMA discord bot that says geek and historical staff phrases and sends ALMA memes.

`saygeek` is taken from [Python port of "official" ALMA saygeek application](https://github.com/bandaangosta/saygeek)

### Commands

    !alma saygeek KEY

where KEY is any from the the following list:

  * ALMA
  * AOG
  * BAD-CONCEPTS
  * BAD-SPANISH
  * BAD-TRANSLATION
  * BYE
  * CONFIRM
  * GOLDEN-JIRA
  * GOLDEN-SVN
  * HELLO
  * HUMOUR
  * MOVIE
  * QUOTE

Example:   

    !alma saygeek GOLDEN-JIRA
    [Notable tickets]:
    ICT-5179 "... I have no sympathy for people complaining about problems in this area ..."

    !alma saygeek AOG    
    [Se dijo en el Control Room alguna vez]:
    ¿no te devolvió la antena?  yo a él lo vi  almorzando en el casino
    
    !alma meme
    <receive an awesome ALMA meme here>
    
### Authorization

File `token.prv` must be placed next to bot.py containing bot token.   
Invite bot to your server by generating an invitation URL at https://discord.com/developers/applications. Then, paste the invitation in a browser. 
You will be asked to select the server where the bot should go.

### Logging

A log file is generated for inspection of events and errors. It defaults to `discord.log` located next to bot.py.

### Memes

Memes location can be set in `config.py`. It defaults to `memes` folder. Files must have `.jpg` and `.png` extension (lowercase).

### Deployment
Bot is just a Python script. Just leave it running somewhere.   
A simple way using Docker is proposed:   

    docker build -t discord-bot .
    docker run -d --restart=always -v /path/to/memes:/app/memes --name discord-bot discord-bot

You may want to create a volume to access log file in an easier way, as well.
