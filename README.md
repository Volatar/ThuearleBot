# ThuearleBot
A privacy focused bot created for Volatar's servers.

# Installation
Create the bot on the discord side and get it's auth token from the bot tab. Place that in a file named ".env" next to
ThuearleBot.py with the following inside, replacing with your token:
```
# .env
DISCORD_TOKEN=yourbottokengoeshere
```

# Features
- /tableflip - Bot will respond with a quip or gif emphasizing the action.
- !heresy - Bot will respond with a heresy detected gif
- !gitgud - Responds with a "Git Gud" or Dark Souls gif

# Editing command responses
To edit the list of possible command responses, edit the appropriately named .txt files in the commands folder, then
run dbcreate.py