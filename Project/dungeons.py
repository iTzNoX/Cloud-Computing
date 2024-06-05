import discord
from discord.ext import commands
import json_database

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.voice_states = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)

current_lobby_ids = []
f1_queue = {}
f2_queue = {}
f3_queue = {}
f4_queue = {}
f5_queue = {}
f6_queue = {}
f7_queue = {}
target_channel = 1243315943736606833
vc = 1243315994273910894
f1 = None
f2 = None
f3 = None
f4 = None
f5 = None
f6 = None
f7 = None

@client.event
async def on_ready():
    print(f"{client.user} Runs")

@client.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.author, discord.Member) and "Developer" in [role.name for role in message.author.roles]:
        if message.content.startswith("!"):
            parts = message.content.split("=")
            command = parts[0].strip()
            value = parts[1].strip()

            if command == "!set f1":
                global f1
                f1 = int(value)
                await message.channel.send(f"successfully set f1")
                print(f"set f1 to {value}")
            if command == "!set f2":
                global f2
                f2 = int(value)
                await message.channel.send(f"successfully set f2")
                print(f"set f2 to {value}")
            if command == "!set f3":
                global f3
                f3 = int(value)
                await message.channel.send(f"successfully set f3")
                print(f"set f3 to {value}")
            if command == "!set f4":
                global f4
                f4 = int(value)
                await message.channel.send(f"successfully set f4")
                print(f"set f4 to {value}")
            if command == "!set f5":
                global f5
                f5 = int(value)
                await message.channel.send(f"successfully set f5")
                print(f"set f5 to {value}")
            if command == "!set f6":
                global f6
                f6 = int(value)
                await message.channel.send(f"successfully set f6")
                print(f"set f6 to {value}")
            if command == "!set f7":
                global f7
                f7 = int(value)
                await message.channel.send(f"successfully set f7")
                print(f"set f7 to {value}")
    else:
        return

@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    global f1, f2, f3, f4, f5, f6, f7
    global f1_queue, f2_queue, f3_queue, f4_queue, f5_queue, f6_queue, f7_queue

    queue_changed = False
    better_queue = False
    opposite_floor = [f1_queue, f2_queue, f3_queue, f4_queue, f5_queue, f6_queue, f7_queue]
    guild = reaction.message.guild
    category_name = "════ Dungeon Queue ════"
    category = discord.utils.get(guild.categories, name=category_name)

    # wenn auf floor 1-7 reacted wird und man in dem vc ist
    if reaction.message.channel.id == target_channel and reaction.message.id in (f1, f2, f3, f4, f5, f6, f7):
        # remove reaction
        await reaction.remove(user)

        # checks for floor queue
        floor_id = reaction.message.id
        if floor_id == f1:
            floor = f1_queue
            opposite_floor.remove(floor)
            queue = "Floor 1"
            for idx, queue in enumerate(opposite_floor):
                if user.name in queue:
                    del queue[user.name]
                    await user.send(f"you have been removed from your old queue and were added to the F1 Queue"
                                    f"theres currently {len(queue)+1} player(s) in queue")
                    queue_changed = True
        elif floor_id == f2:
            floor = f2_queue
            opposite_floor.remove(floor)
            queue = "Floor 2"
            for idx, queue in enumerate(opposite_floor):
                if user.name in queue:
                    del queue[user.name]
                    await user.send(f"you have been removed from your old queue and were added to the F2 Queue"
                                    f"theres currently {len(queue)+1} player(s) in queue")
                    queue_changed = True
        elif floor_id == f3:
            floor = f3_queue
            opposite_floor.remove(floor)
            queue = "Floor 3"
            for idx, queue in enumerate(opposite_floor):
                if user.name in queue:
                    del queue[user.name]
                    await user.send(f"you have been removed from your old queue and were added to the F3 Queue"
                                    f"theres currently {len(queue)+1} player(s) in queue")
                    queue_changed = True
        elif floor_id == f4:
            floor = f4_queue
            opposite_floor.remove(floor)
            queue = "Floor 4"
            for idx, queue in enumerate(opposite_floor):
                if user.name in queue:
                    del queue[user.name]
                    await user.send(f"you have been removed from your old queue and were added to the F4 Queue"
                                    f"theres currently {len(queue)+1} player(s) in queue")
                    queue_changed = True
        elif floor_id == f5:
            floor = f5_queue
            opposite_floor.remove(floor)
            queue = "Floor 5"
            better_queue = True
            for idx, queue in enumerate(opposite_floor):
                if user.name in queue:
                    del queue[user.name]
                    await user.send(f"you have been removed from your old queue and were added to the F5 Queue"
                                    f"theres currently {len(queue)+1} player(s) in queue")
                    queue_changed = True
        elif floor_id == f6:
            floor = f6_queue
            opposite_floor.remove(floor)
            queue = "Floor 6"
            better_queue = True
            for idx, queue in enumerate(opposite_floor):
                if user.name in queue:
                    del queue[user.name]
                    await user.send(f"you have been removed from your old queue and were added to the F6 Queue"
                                    f"theres currently {len(queue)+1} player(s) in queue")
                    queue_changed = True
        elif floor_id == f7:
            floor = f7_queue
            opposite_floor.remove(floor)
            queue = "Floor 7"
            better_queue = True
            for idx, queue in enumerate(opposite_floor):
                if user.name in queue:
                    del queue[user.name]
                    await user.send(f"you have been removed from your old queue and were added to the F7 Queue"
                                    f"theres currently {len(queue)+1} player(s) in queue")
                    queue_changed = True
        else:
            print("no floor found")
            return

        if user.voice and user.voice.channel and user.voice.channel.id == vc:
            member = reaction.message.guild.get_member(user.id)

            if member:

                new_nickname = member.display_name

                # Checkt nach reaction um namen und queue zu managen
                if reaction.emoji.id == 1244818415160528979:
                    # dels from queue if reacts with same role on same queue
                    if user.name in floor and floor[user.name] == f":Berserk:{str(reaction.emoji.id)}":
                        del floor[user.name]
                        await user.send("you have been removed from the queue")
                        return
                    # changes role when reacts with diffrent role on same queue
                    elif user.name in floor and not floor[user.name] == f":Berserk:{str(reaction.emoji.id)}":
                        new_nickname += " :Berserk:1244818415160528979"
                        floor[user.name] = ":Berserk:1244818415160528979"
                        await user.send("your role has been changed")
                        queue_changed = True
                    # if user is no no queue at all
                    new_nickname += " :Berserk:1244818415160528979"
                    floor[user.name] = ":Berserk:1244818415160528979"
                    print("added to queue")
                elif reaction.emoji.id == 1244811672506597440:
                    if user.name in floor and floor[user.name] == f":Archer:{str(reaction.emoji.id)}":
                        del floor[user.name]
                        await user.send("you have been removed from the queue")
                        return
                    elif user in floor and not floor[user.name] == f":Archer:{str(reaction.emoji.id)}":
                        new_nickname += " :Archer:1244811672506597440"
                        floor[user.name] = ":Archer:1244811672506597440"
                        await user.send("your role has been changed")
                        queue_changed = True
                    new_nickname += " :Archer:1244811672506597440"
                    floor[user.name] = ":Archer:1244811672506597440"
                    print("added to queue")
                elif reaction.emoji.id == 1244811630093664307:
                    if user.name in floor and floor[user.name] == f":Tank:{str(reaction.emoji.id)}":
                        del floor[user.name]
                        await user.send("you have been removed from the queue")
                        return
                    elif user.name in floor and not floor[user.name] == f":Tank:{str(reaction.emoji.id)}":
                        new_nickname += " :Tank:1244811630093664307"
                        floor[user.name] = ":Tank:1244811630093664307"
                        await user.send("your role has been changed")
                        queue_changed = True
                    new_nickname += " :Tank:1244811630093664307"
                    floor[user.name] = ":Tank:1244811630093664307"
                    print("added to queue")
                elif reaction.emoji.id == 1244811658396827658:
                    if user.name in floor and floor[user.name] == f":Mage:{str(reaction.emoji.id)}":
                        del floor[user.name]
                        await user.send("you have been removed from the queue")
                        return
                    elif user.name in floor and not floor[user.name] == f":Mage:{str(reaction.emoji.id)}":
                        new_nickname += " :Mage:1244811658396827658"
                        floor[user.name] = ":Mage:1244811658396827658"
                        await user.send("your role has been changed")
                        queue_changed = True
                    new_nickname += " :Mage:1244811658396827658"
                    floor[user.name] = ":Mage:1244811658396827658"
                    print("added to queue")
                elif reaction.emoji.id == 1244811684204515338:
                    if user.name in floor and floor[user.name] == f":Healer:{str(reaction.emoji.id)}":
                        del floor[user.name]
                        await user.send("you have been removed from the queue")
                        return
                    elif user.name in floor and not floor[user.name] == f":Healer:{str(reaction.emoji.id)}":
                        new_nickname += " :Healer:1244811684204515338"
                        floor[user.name] = ":Healer:1244811684204515338"
                        await user.send("your role has been changed")
                        queue_changed = True
                    new_nickname += " :Healer:1244811684204515338"
                    floor[user.name] = ":Healer:1244811684204515338"
                    print("added to queue")
                else:
                    print("role not found")
                    return

                # pn dass man der queue gejoint ist
                if not queue_changed:
                    await user.send(f"you successfully joined the party finder v2 Queue, "
                                    f"there is currently {len(floor)} player(s) in the queue")

                try:
                    # changed user nickname to show their class
                    await member.edit(nick=new_nickname)
                except:
                    print("Owner rename issue")

                valid_players = get_valid_players(floor)

                # wenn 5 leute in der queue 5-7 sind, move zusammen--------------------------
                if len(valid_players) == 5 and better_queue == True:
                    player = list(valid_players.keys())

                    # channel erstellen
                    if category:
                        new_channel = await guild.create_voice_channel(f"{queue} Lobby", category=category)
                        new_channel_id = new_channel.id
                        current_lobby_ids.append(new_channel_id)
                    else:
                        print("Category not found")

                    # moves first 5 players in queue
                    if new_channel is not None:
                        for i in range(5):
                            await player[i].move_to(new_channel)

                        # removes first 5 players from low_queue
                        players = list(floor.items())
                        players[5:]

                    else:
                        print(f"Channel {new_channel_id} not found")
                # wenn 5 leute in der queue 1-4 sind, move zusammen--------------------------
                elif len(floor) == 5:
                    player = list(floor.keys())

                    # channel erstellen
                    if category:
                        new_channel = await guild.create_voice_channel(f"{queue} Lobby", category=category)
                        new_channel_id = new_channel.id
                        current_lobby_ids.append(new_channel_id)
                    else:
                        print("Category not found")

                    # moves first 5 players in queue
                    if new_channel is not None:
                        for i in range(5):
                            await player[i].move_to(new_channel)

                        # removes first 5 players from low_queue
                        players = list(floor.items())
                        players[5:]

                    else:
                        print(f"Channel {new_channel_id} not found")
                # ----------------------------------------------------------------------------
        else:
            await user.send("join the party finder voice channel before you try to queue. "
                            "you are muted inside the channel, but its needed for us to be able to move you")
    else:
        return

@client.event
async def on_voice_state_update(member, before, after):
    # deletes temp channels if empty
    if before.channel is not None and before.channel.id in current_lobby_ids:
        for lobby_id in current_lobby_ids:
            channel = client.get_channel(lobby_id)
            if channel and len(channel.members) == 0:
                await channel.delete()
    try:
        # changes their name back to normal if they leave queue
        if before.channel is not None and before.channel.id == 1243315994273910894:
            role_names = [":Berserk:", ":Archer:", ":Tank:", ":Mage:", ":Healer:"]
            new_nickname = member.display_name
            for role in role_names:
                new_nickname = new_nickname.replace(role, "")

            global f1_queue, f2_queue, f3_queue, f4_queue, f5_queue, f6_queue, f7_queue

            #dels them out of queue
            if member.name in f1_queue:
                del f1_queue[member.name]
                await member.edit(nick=new_nickname.strip())
                await member.send("You have left the queue")
            elif member.name in f2_queue:
                del f2_queue[member.name]
                await member.edit(nick=new_nickname.strip())
                await member.send("You have left the queue")
            elif member.name in f3_queue:
                del f3_queue[member.name]
                await member.edit(nick=new_nickname.strip())
                await member.send("You have left the queue")
            elif member.name in f4_queue:
                del f4_queue[member.name]
                await member.edit(nick=new_nickname.strip())
                await member.send("You have left the queue")
            elif member.name in f5_queue:
                del f5_queue[member.name]
                await member.edit(nick=new_nickname.strip())
                await member.send("You have left the queue")
            elif member.name in f6_queue:
                del f6_queue[member.name]
                await member.edit(nick=new_nickname.strip())
                await member.send("You have left the queue")
            elif member.name in f7_queue:
                del f7_queue[member.name]
                await member.edit(nick=new_nickname.strip())
                await member.send("You have left the queue")
    except:
        print("Owner Issue")

def get_valid_players(floor):
    valid_players = {}
    archer_count = 0
    tank_count = 0
    count = 0

    for player, role in floor.items():
        if count >= 5:
            break
        if role == "Archer" and archer_count < 1:
            valid_players[player] = role
            archer_count += 1
            count += 1
        elif role == "Tank" and tank_count < 1:
            valid_players[player] = role
            tank_count += 1
            count += 1
        elif role not in ["Archer", "Tank"]:
            valid_players[player] = role
            count += 1

    return valid_players

client.run("MTI0NzkyNzAxODU3OTAzODI3OA.G6W59m.a6JMkmBHooSvt56u7PNJQRe8R7tLRhWXedpYs0")

#TODO
# Done

# HOW TO USE
# send Floor 1-7 Messages into chat and react with class reactions
# (:Berserk:, :Mage:, :Healer:, :Tank:, :Archer:)
# use !set f1-7 = message_id using the message ids of floor 1 - 7 messages
# join pf queue and react with your role on your desired floor
# wait for enough people to join the queue and get moved into your lobby
# react with your role again or leave the vc to dequeue
# react on another role to change your role but keep your place in queue

# DEBUGGING
# emoji remove when lobby left