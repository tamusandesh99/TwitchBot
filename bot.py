import json
from twitchio.ext import commands
import config
import random
import time

""" Initializing the bot """
bot = commands.Bot(
    token=config.TMI_TOKEN,
    client_id=config.CLIENT_ID,
    nick=config.BOT_NICK,
    prefix=config.BOT_PREFIX,
    initial_channels=[config.CHANNEL],
)


def get_count():
    """ Reads the count from the JSON file and returns it """
    with open(config.JSON_FILE) as json_file:
        data = json.load(json_file)
        return data['total_run']


# def get_counter_status():
#     """ Reads the count status (stop or start) from the JSON file and returns it """
#     with open(config.JSON_FILE) as json_file:
#         data = json.load(json_file)
#         return data['stop_counter']
#
#
def update_send_run():
    with open(config.JSON_FILE) as json_file:
        data = json.load(json_file)
        data['send_run'] = False
    with open(config.JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)


def check_if_send_total_run():
    with open(config.JSON_FILE) as json_file:
        data = json.load(json_file)
        return data['send_run']


@bot.event()
async def event_ready():
    print('Bot is ready with run of: ' + str(get_count()))


@bot.event()
async def event_message(ctx):
    try:
        print(ctx.author.name + ": " + ctx.content)
    except:
        await bot.handle_commands(ctx)


""" this runs in infinite loop. Checks weather to send the run count on chat or not from json file """
# @bot.event()
# async def event_ready():
#     try:
#         while True:
#             if check_if_send_total_run():
#                 print("this is true")
#                 # time.sleep(3)
#                 # await bot.connected_channels[0].send('Total run: ' + str(get_count()))
#                 update_send_run()
#                 time.sleep(3)
#
#     except:
#         print('Error in sending messsage')


# Returns the rules for roll commands
@bot.command(name="rules")
async def rules(ctx):
    await ctx.send("Rules are simple: if you roll odd, your points get divided. If even then multiplied. You start "
                   "with 100")


# Mod can add points to the users in chat
@bot.command(name="add")
async def addPoints(ctx, user_name, points):
    if ctx.author.name == 'boco6969':
        with open(config.POINTS_FILE) as json_file:
            users_data = json.load(json_file)
        if user_name in users_data:
            add_points = int(users_data[user_name]) + int(points)
            users_data[user_name] = add_points
            with open(config.POINTS_FILE, 'w') as json_file:
                json.dump(users_data, json_file, sort_keys=True, indent=4, separators=(',', ': '))
            await ctx.send("Added " + points + " points to " + "@" + user_name)
        else:
            await ctx.send(user_name + " is not in the database boss")
    else:
        await ctx.send("@"+ctx.author.name+" You are not Boco")


# Checks if the bot is connected to the chat
@bot.command(name="check")
async def check(ctx):
    await ctx.send("@" + ctx.author.name + " Im here")


# Gets the points for the users that used the points command with the prefix
@bot.command(name="points")
async def get_points(ctx):
    with open(config.POINTS_FILE) as json_file:
        users_data = json.load(json_file)
    if ctx.author.name in users_data:
        print(users_data[ctx.author.name])
        send_points = int(users_data[ctx.author.name])
        await ctx.send("@" + ctx.author.name + " Your points: " + str(send_points))
    else:
        users_data[ctx.author.name] = 100
        with open(config.POINTS_FILE, 'w') as json_file:
            json.dump(users_data, json_file, sort_keys=True, indent=4, separators=(',', ': '))
        await ctx.send("@" + ctx.author.name + "." + " Your points: " + str(100))


# Rolls dice, 1-6. If it lands odd, point gets divided, even is multiplied
@bot.command(name="roll")
async def roll_dice(ctx, arg):
    with open(config.POINTS_FILE) as json_file:
        users_data = json.load(json_file)
    if ctx.author.name in users_data:
        user_point = users_data[ctx.author.name]
        random_roll = random.randint(0, 6)
        user_point_int = int(user_point)
        argument_int = int(arg)

        if user_point_int < argument_int:
            await ctx.send("@" + ctx.author.name + ". Your total point is: "
                           + str(int(user_point)) + ". " + "Roll lower.")
        else:
            if random_roll % 2 == 0:
                user_point = user_point * random_roll
                print(user_point)
            else:
                user_point = user_point / random_roll
                # print(user_point)
            users_data[ctx.author.name] = user_point
        with open(config.POINTS_FILE, 'w') as json_file:
            json.dump(users_data, json_file, sort_keys=True, indent=4, separators=(',', ': '))
        await ctx.send("@" + ctx.author.name + " rolled " + str(random_roll) + "." + " Total points: " +
                       str(int(users_data[ctx.author.name])))
    else:
        await ctx.send("@" + ctx.author.name + "." + " You don't have points. Do !points to add points")


@bot.command(name='attempts')
async def sendRun_command(ctx):
    print("pp")
    await ctx.send(str(get_count()))


@bot.command(name='challenges')
async def test_command(ctx):
    try:
        await ctx.send("Brett is the god")
    except:
        print('error')


@bot.command(name='fist')
async def test_command(ctx):
    await ctx.send("Fisted so far: Radagon, Maliketh, Radahn, Margit, Morgott")


@bot.command(name='streamMind')
async def test_command(ctx):
    await ctx.send("Yep. Its Golan and she VIP too")


@bot.command(name='whoisW')
async def test_command(ctx):
    await ctx.send("Its Jake. W Jake")


@bot.command(name='babyname')
async def test_command(ctx):
    await ctx.send("Fire Giant")


if __name__ == '__main__':
    bot.run()
