# Discrypto
Decrypto Discord Bot

# How to play with the bot

Looks for keyword `d ` in the discord servers the bot is added to (this is changeable at the top of dw.py)

Run `d h` or `d help` to get started. The main commands you'll need are `d reset`, `d addme` (run by all players), `d startgame`, `d draw`, `d reveal`, `d timer`, and `d endgame`.

# How to run the bot

Run by installing requirements in requirements.txt and running dw.py (Written in Python 3.7).

You'll need to include a file named `secrets.py` that implements the following function in order to run:

```
def get_token():
    token = "PUT_YOUR_DISCORD_BOT_TOKEN_HERE"
    return token
```
