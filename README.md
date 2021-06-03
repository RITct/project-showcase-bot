# project-showcase-bot

A discord bot to help showcase your projects


### What does this do?

This bot aids in creating a showcase channel for your discord server.

Server admins could react with a preconfigured emoji to github links to add them to the showcase channel.

Then the bot add this github link along with description, title, issues, stars and forks to a showcase channel. 

If the owner of the repo adds a webhook to this bot, all these stats would be updated live.

### Usage

1. Add this bot via this [link](https://discord.com/api/oauth2/authorize?client_id=846073659293433856&permissions=67584&scope=bot)
2. Set your project showcase channel with `$set_target_channel <LINK_TO_CHANNEL>` command.
3. Ensure bot has write access to your project showcase channel.
4. Admins can now react with :star_struck: to a github link to add it to showcase channel
5. Owner of the repo can integrate a github webhook if they want to receive live changes in discord server. 
 
