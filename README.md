# project-showcase-bot

A discord bot to help showcase your projects


### What does this do?

This bot aids in creating a showcase channel for your discord server.

Server admins could react with a preconfigured emoji to github links to add them to the showcase channel.

Then the bot add this github link along with description, title, issues, stars and forks to a showcase channel. 

If the owner of the repo adds a webhook to this bot, all these stats would be updated live.

### Usage

1. Set your environment variables(refer example env file).
2. Configure your emojis in `app/config.py`.
3. Add bot to your server.
4. Ensure bot has write access to your project showcase channel.
 
