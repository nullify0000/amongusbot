import discord
from discord.ext import commands

# Extension Definitions 
extentions = [ "Commands", "MessageEvents", "VoiceEvents", "ServerEvents" ]

if __name__ == "__main__":
    
    # Setup client with prefix
    client = commands.Bot(command_prefix = '.')

    for extension in extentions:
        try:
            client.load_extension(f'cogs.{extension}')
            print(f'[+] Loaded extension: {extension}')
        except Exception as E:
            print(f'[-] Failed to load extension: {extension}')

    client.run('')