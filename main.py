import discord
from discord.ext import commands

prefix = "o."
bot = commands.Bot(command_prefix=prefix, self_bot=True, case_insensitive=True, help_command=None)

token = "token here"
userids = []
global start_sawtar
start_sawtar = False

    
@bot.event
async def on_ready():
    print(f"Linker ready: Connected as {bot.user.name}#{bot.user.discriminator}")

@bot.command(name="add", description="Adds users to the DM Session")
async def _add(ctx, user: discord.User = None):
    await ctx.message.delete()
    if user is None:
        await ctx.send("Please specify a user")
    id = user.id
    userids.append(id)
    user = await bot.fetch_user(id)
    msg = f"Added {user.name}#{user.discriminator} to the DM session"
    await ctx.send(msg, delete_after=60)

@bot.command(name="remove", description="Removes users from the DM Session")
async def _remove(ctx, user: discord.User = None):
    await ctx.message.delete()
    if user is None:
        await ctx.send("Please specify a user")
    id = user.id
    if id in userids:
        userids.remove(id)
    user = await bot.fetch_user(id)
    msg = f"Removed {user.name}#{user.discriminator} from the DM session"
    await ctx.send(msg, delete_after=60)

@bot.command(name="help", description="Displays the help command")
async def _help(ctx):
    await ctx.message.delete()
    msg = "```\nCommands listed here.\n"
    for command in bot.walk_commands():
        msg += f"{command.name} :   {command.description}\n"
    msg += "```"
    await ctx.send(msg, delete_after=60)
    

@bot.command(name="list", description="Displays the users in the DM Session")
async def _list(ctx):
    await ctx.message.delete()
    em = discord.Embed()
    msg = f"```\n{bot.user.name}'s DM list:"
    for i in userids:
        user = await bot.fetch_user(i)
        msg += f"{user.name}#{user.discriminator}\n"
    msg += "```"
    await ctx.send(msg, delete_after=60)

@bot.command(name="start", description="Starts the DM Session")
async def _start(ctx):
    await ctx.message.delete()
    global start_sawtar
    start_sawtar = True
    msg = f"Started the DM for {len(userids)} users"
    await ctx.send(msg, delete_after=60)

@bot.command(name="removeall", aliases=['rall'], description="Removes all users from the DM Session")
async def _removeall(ctx):
    await ctx.message.delete()
    userids.clear()
    msg = f"Removed all ids from the list"
    await ctx.send(msg, delete_after=60)
    

@bot.command(name="stop", description="Stops the DM Session")
async def _stop(ctx):
    await ctx.message.delete()
    global start_sawtar
    start_sawtar = False
    msg = f"Stopped the DM session for {len(userids)} users"
    await ctx.send(msg, delete_after=60)

@bot.event
async def on_message(message):
    global start_sawtar
    if start_sawtar == True:
        if ( isinstance(message.channel, discord.DMChannel) and message.author.id in userids):
            for id in userids:
                try:
                    sender = message.author.id
                    if sender == id:
                        pass
                    else:
                        sender = await bot.fetch_user(message.author.id)
                        user_1 = await bot.fetch_user(id)
                        async for mesg in message.channel.history(limit=1):
                            if len(mesg.attachments) == 0:
                                await user_1.send(f"`{sender.name}:  {str(mesg.clean_content)}`")
                            else:
                                attachments = mesg.attachments
                                links = ""
                                for attachment in attachments:
                                    links += attachment.url + "\n"
                                    await user_1.send(f"`{sender.name}:  {str(mesg.clean_content)}`\n **Attachments:**{links}")
                except Exception as e:
                        print(f'[ERROR] Couldn\'t send message to {user_1.name} \n{e}')

                        
    await bot.process_commands(message)









bot.run(token, bot=False)
