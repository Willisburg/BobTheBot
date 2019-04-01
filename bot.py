import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import asyncio
import requests
import os

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='!verify'))
    print('Bob The Bot v1.0 --')
    print('Successfully joined account: ' + bot.user.name)

@bot.command(pass_context=True)
async def np(ctx, *arg):
    message = ctx.message;
    channel = message.channel;
    member = message.author;
    await bot.send_message(channel, "no problem :D");
    
    
    
@bot.command(pass_context=True)
async def verify(ctx, *arg):
    message = ctx.message;
    channel = message.channel;
    member = message.author;
    
    if "529724186982350868" in [y.id for y in member.roles]:
        await bot.send_message(channel, "You're already a verified user.");
    else:
        try:
            if(arg[0].startswith("/u/")):
                username = arg[0][1:len(arg[0])]
            else:
                username = arg[0]
            url='https://old.reddit.com/'+username+'/about.json';
            header={'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
            r=requests.get(url=url, headers=header);
            try:
                data = r.json()['data']['subreddit']['public_description'];
                try:
                    scraped=int(data);
                    if(scraped==int(member.id)):
                        try:
                            role = discord.utils.get(member.server.roles, id="529724186982350868")
                            await bot.add_roles(member, role);
                            await bot.change_nickname(member, username)
                            await bot.send_message(channel, "You're now a verified user!");
                        except:
                            await bot.send_message(channel, "Sorry i don't have permissions to give roles or change nicknames.");
                    else:
                        await bot.send_message(channel, "Change your reddit profile description to "+str(member.id)+" and run this command again!");
                except:
                    await bot.send_message(channel, "Change your profile description to "+str(member.id)+" and run this command again!");
            except:
                await bot.send_message(channel, "I wasn't able to find a reddit account with that username, or the reddit account is old, please update or wait for the bot to update.");
        except:
            await bot.send_message(channel, "Please follow the form of ``!verify u/username`` and try again.");

bot.run(str(os.environ.get('BOT_TOKEN')))          
