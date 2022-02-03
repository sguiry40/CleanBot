import discord
from discord.enums import Status
from discord.ext import commands
import random
import os

activity = discord.Game(name="+help")
bot = commands.Bot(command_prefix = '+', help_command=None,activity=activity,Status=discord.Status.online)

@bot.event
async def on_ready():
    print("CleanBot is online.")


@bot.command()
async def create(ctx):
    # if the list exists, do nothing
    if os.path.exists("C:\\Users\\sguir\\DiscordBots\\CleanBot\\" + str(ctx.guild.id) + ".txt"):
        await ctx.send("The server specific list already exists!")
    # else create the list
    else:
        file1 = open("C:\\Users\\sguir\\DiscordBots\\CleanBot\\" + str(ctx.guild.id) + ".txt", "w+")
        await ctx.send("Server specific list created!")

@bot.command()
async def clear(ctx):
    # create new list
    file1 = open("C:\\Users\\sguir\\DiscordBots\\CleanBot\\" + str(ctx.guild.id) + ".txt", "w+")
    await ctx.send("Server specific list cleared")


@bot.command()
async def help(ctx):
    embed = discord.Embed(title = "List of commands", color=discord.Color.blue(), description = "Please begin by using the "
    + "+create command to create your server specific list")
    embed.add_field(name = "+add <word>", value = "adds a new word to the banned list", inline = True)
    embed.add_field(name = "+remove <word>", value = "removes a word from the banned list", inline = True)
    embed.add_field(name = "+list", value = "shows the current banned list", inline = True)
    embed.add_field(name = "+clear", value = "clears all words off the banned list", inline = True)

    await ctx.send(embed=embed)

@bot.command()
async def list(ctx):
    try:
        file1 = open("C:\\Users\\sguir\\DiscordBots\\CleanBot\\" + str(ctx.guild.id) + ".txt", "r")
    except FileNotFoundError:
        await ctx.send("Server list does not exist! Please use the +create command to begin.")
        return

    lines = file1.readlines()

    if len(lines) == 0:
        await ctx.send("There are no words on the banned list!")
        return

    bannedWords = ""

    for line in lines:
        bannedWords = bannedWords + "||" + line.strip("\n") + "||\n"

    embed = discord.Embed(title = "List of banned words:", description = bannedWords, color = discord.Color.blue()) 

    await ctx.send(embed=embed)      

@bot.command()
async def remove(ctx, word: str):
    if not word.isalpha():
        await ctx.send("Please make sure the word only contains alphabetical characters.")
        return

    try:
        file1 = open("C:\\Users\\sguir\\DiscordBots\\CleanBot\\" + str(ctx.guild.id) + ".txt", "r")
    except FileNotFoundError:
        await ctx.send("Server list does not exist! Please use the +create command to begin.")
        return

    lines = file1.readlines()
    file1.close()

    if (not word.lower() + "\n" in lines):
        await ctx.send("This word is not in the banned list!")
        return

    file2 = open("C:\\Users\\sguir\\DiscordBots\\CleanBot\\" + str(ctx.guild.id) + ".txt", "w")

    for line in lines:
        if line.strip("\n") != word.lower():
            file2.write(line)

    file2.close()
    await ctx.send("This word has been removed from the banned list! You may delete your message if desired.")

@bot.command()
async def add(ctx, word: str):
    if not word.isalpha():
        await ctx.send("Please make sure the word only contains alphabetical characters.")
        return

    try:
        file1 = open("C:\\Users\\sguir\\DiscordBots\\CleanBot\\" + str(ctx.guild.id) + ".txt", "r+")
    except FileNotFoundError:
        await ctx.send("Server list does not exist! Please use the +create command to begin.")
        return

    lines = file1.readlines()

    if word + "\n" in lines:
        await ctx.send("This word is already on the banned list!")
        return 

    file1.write(word.lower() + "\n")
    file1.close()

    await ctx.send("The word has been added to the banned list! You may delete your message if desired.")

@bot.event
async def on_message(message):
    if message.author.name == "CleanBot":
        return

    if (message.content.startswith('+add') or message.content.startswith('+remove') or
        message.content.startswith('+list') or message.content.startswith('+help') or
        message.content.startswith('+create') or message.content.startswith('+clear')):
        await bot.process_commands(message)
        return

    words = message.content.strip(" ").lower()

    try:
        file1 = open("C:\\Users\\sguir\\DiscordBots\\CleanBot\\" + str(message.guild.id) + ".txt", "r")
    except FileNotFoundError:
        return

    lines = file1.readlines()

    titles = ["Easy there!", "Careful!", "Whoa there!", "Chill out!", "Oh no!", "Watch your mouth!", "Oh NAH!"]

    for line in lines:
        if line.strip("\n") in words:

            embed = discord.Embed(title = random.choice(titles), color = discord.Color.blue(), description = "You just used a banned word! Please "
            + "be more careful. The word was: ||" + line.strip("\n") + "||")
            await message.channel.send(embed=embed)
            file1.close()
            return
    
    file1.close()

#bot.run(token)
