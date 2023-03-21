import json
from twitchio.ext import commands
import config
import random

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


def get_counter_status():
    """ Reads the count status (stop or start) from the JSON file and returns it """
    with open(config.JSON_FILE) as json_file:
        data = json.load(json_file)
        return data['stop_counter']


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
    print(ctx.author.name)
    print(ctx.content)
    await bot.handle_commands(ctx)


# @bot.event()
# async def event_ready():
#     try:
#         while True:
#             if check_if_send_total_run():
#                 print("this is true")
#                 time.sleep(3)
#                 await bot.connected_channels[0].send('Total run: ' + str(get_count()))
#                 update_send_run()
#
#     except:
#         print('Error in sending messsage')
#     time.sleep(3)

@bot.command(name="test")
async def test_command(ctx):
    print("test")


@bot.command(name="points")
async def get_points(ctx):
    with open(config.POINTS_FILE) as json_file:
        users_data = json.load(json_file)
    if ctx.author.name in users_data:
        print(users_data[ctx.author.name])
    else:
        users_data[ctx.author.name] = 6
        with open(config.POINTS_FILE, 'w') as json_file:
            json.dump(users_data, json_file, sort_keys=True, indent=4, separators=(',', ': '))


@bot.command(name="roll")
async def roll_dice(ctx):
    with open(config.POINTS_FILE) as json_file:
        users_data = json.load(json_file)
    if ctx.author.name in users_data:
        user_point = users_data[ctx.author.name]
        random_roll = random.randint(0, 6)
        print(random_roll)
        if random_roll % 2 == 0:
            user_point = user_point * random_roll
            print(user_point)
        else:
            user_point = user_point / random_roll
            print(user_point)
        users_data[ctx.author.name] = user_point
        with open(config.POINTS_FILE, 'w') as json_file:
            json.dump(users_data, json_file, sort_keys=True, indent=4, separators=(',', ': '))
        await ctx.send(str(users_data[ctx.author.name]))


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
