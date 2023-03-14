import json
from twitchio.ext import commands
import config

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


run = get_count()


@bot.event()
async def event_ready():
    print('Bot is ready with run of: ' + str(run))


@bot.event()
async def event_message(ctx):
    print(ctx.author)
    print(ctx.content)
    await bot.handle_commands(ctx)


@bot.command(name='attempts')
async def sendRun(ctx):
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


