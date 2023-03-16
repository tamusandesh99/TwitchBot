import json
from twitchio.ext import commands
import config
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


run = get_count()


@bot.event()
async def event_ready():
    print('Bot is ready with run of: ' + str(run))


@bot.event()
async def event_ready():
    while True:
        try:
            if check_if_send_total_run():
                print("this is true")
                await bot.connected_channels[0].send('Total run: ' + str(get_count()))
                update_send_run()
        except:
            print('Error in sending messsage')
        time.sleep(3)


@bot.event()
async def event_message(ctx):
    print(ctx.author)
    print(ctx.content)
    await bot.handle_commands(ctx)


@bot.command(name='attempts')
async def sendRun_command(ctx):
    await ctx.send(str(get_count()))


@bot.command(name='challenges')
async def test_command(ctx):
    await ctx.send("Brett is the god")


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
    # sendRun_automatic()
