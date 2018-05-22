import discord
import asyncio
import tweepy
import platform
import keys
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import urllib.request


client = Bot(description="This bot is for Kermit House of Shitposting to tweet.", command_prefix="&", pm_help = False)
client.remove_command("help")

class Bot_Func:
    @commands.cooldown(1, 30, commands.BucketType.user)
    @client.command(pass_context = True)
    @commands.has_any_role('Virgins')
    async def post(ctx, *, tweet_text):
        final_text = str(ctx.message.author) + ': ' + tweet_text
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        api.update_status(status=final_text)
        print(Status.url)
        await client.say("Successfully tweeted!\nCheck out it here: https://twitter.com/KShitpostbot")

    @commands.cooldown(1, 30, commands.BucketType.user)
    @client.command(pass_context = True)
    @commands.has_any_role('Virgins')
    async def upload(ctx, *, tweet_text, url: str=None):
        pic_name = str(ctx.message.channel.id)+'.png'
        final_text = str(ctx.message.author) + ': ' + tweet_text
        await Bot_Func.get_attachment_images(ctx, url)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        api.update_with_media(pic_name, status=final_text)
        await client.say("Successfully tweeted!\nCheck out it here: https://twitter.com/KShitpostbot")

    @client.event
    async def on_command_error(error, ctx):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(description=str(error))
            embed.set_author(name=ctx.message.author)
            embed.colour = ctx.message.author.colour if hasattr(ctx.message.author, "colour") else discord.Colour.default()
            await client.send_message(ctx.message.channel, embed=embed)
        if isinstance(error, commands.CheckFailure):
            await client.send_message(ctx.message.channel, "You have to get the **Virgins** role to use this bot.")


    async def get_attachment_images(ctx, url):
        last_attachment = url
        if url:
            if Functions.is_image(url) is False:
                url = None
        if url is None:
            async for m in client.logs_from(ctx.message.channel, before=ctx.message, limit=20):
                if m.attachments:
                    try:
                        last_attachment = m.attachments[0]['url']
                    except KeyError:
                        continue
                    break
                elif m.embeds:
                    try:
                        last_attachment = m.embeds[0]['url']
                    except KeyError:
                        continue
                    if not Functions.is_image(last_attachment):
                        continue
                    else:
                        break
        pic_name = str(ctx.message.channel.id)+'.png'
        headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        f = urllib.request.Request(url=last_attachment,headers=headers)
        f = urllib.request.urlopen(f)
        with open(pic_name, "wb") as c:
            c.write(f.read())

class Functions():

    def is_image(url):
        extensions = ['jpg', 'png', 'jpeg']
        length = len(url)
        index = 1
        for x in range(2, length):
            if url[-x] == ".":
                break
            else:
                index+=1
        ext = url[-index:].lower()
        if ext not in extensions:
            return False
        else:
            return True

def main():
    @client.event
    async def on_ready():
    	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    	print('--------')
    	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    	print('--------')
    	print('Use this link to invite {}:'.format(client.user.name))
    	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    	print('--------')
    	print('--------')

    client.run(kermit_shitpostbot_token)

if __name__ == "__main__":
    main()
