import discord
from discord.ext import commands
import random

# VoiceEvents Settings
channel_names = [ "🔊 Lobby #1", "🔊 Lobby #2", "🔊 Lobby #3" ]
channel_ids = [ 757726171080294430, 757726296431263826, 757735428936958092 ]
lobby_starter_ids = [ 0, 0, 0, 0 ]

class VoiceEvents(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        # Check for actual channel move, join or disconnect
        if (before.channel == after.channel):
            return

        if (before.channel):
            for idx, channel_name in enumerate(channel_names):

                # Find channel
                if (before.channel.name == channel_name):
                    channel = self.client.get_channel(channel_ids[idx])
                    await channel.set_permissions(member, read_messages=False, send_messages=False, read_message_history=False)
                    
                    if (len(before.channel.members) == 0):
                        lobby_starter_ids[idx] = 0
                        await channel.purge()
                        print(f'{before.channel} now has {len(before.channel.members)} members, removing ownership, purging channel')
                    else:
                        random_member = before.channel.members[random.randrange(0, len(before.channel.members))]
                        if (lobby_starter_ids[idx] == member.id and lobby_starter_ids[idx] != random_member.id):
                            lobby_starter_ids[idx] = random_member.id
                            await channel.send(random_member.mention + " is the new lobby owner.")
                            print(f'{before.channel} now has a new lobby owner: {random_member.name}')

        if (after.channel):
            for idx, channel_name in enumerate(channel_names):
                if (after.channel.name == channel_name):
                    channel = self.client.get_channel(channel_ids[idx])

                    # Purge channel if new lobby
                    if (len(after.channel.members) == 1):
                        await channel.purge()
                        await channel.send(":tada: Purged channel! " + member.mention + ", you're the lobby starter.\n\n**Available commands:** `.host [CODE] [REGION]`\n\n`Please post all lobby codes in this chat!`")
                        lobby_starter_ids[idx] = member.id
                    
                    await channel.set_permissions(member, read_messages=True, send_messages=True, read_message_history=True)

def setup(client):
    client.add_cog(VoiceEvents(client))