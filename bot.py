import json
import random

from twitchio.ext import commands
from pymongo.mongo_client import MongoClient
import configuration
import requests


""" Initializing the bot """
bot = commands.Bot(
    token=configuration.TMI_TOKEN,
    client_id=configuration.CLIENT_ID,
    nick=configuration.BOT_NICK,
    prefix=configuration.BOT_PREFIX,
    initial_channels=[configuration.CHANNEL],
)


# Connecting to mongodb atlas database
uri = "mongodb+srv://" + configuration.MONGODB_USERNAME + ":" + configuration.MONGODB_PASSWORD + \
          "@twitch.5dlmhjq.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
my_database = client.Twitch
all_runs = my_database.Runs
all_users = my_database.points


# gets run count from json file
def get_count():
    """ Reads the count from the JSON file and returns it """
    with open(configuration.JSON_FILE) as json_file:
        data = json.load(json_file)
        return data['total_run']


# Stops the loop in BotLoop file. Stops sending messages
@bot.command(name="stop")
async def stop_loop(ctx):
    if ctx.author.name == 'boco6969':
        with open(configuration.JSON_FILE) as json_file:
            check_status_of_loop = json.load(json_file)
        check_status_of_loop['stop_loop'] = True
        with open(configuration.JSON_FILE, 'w') as json_file:
            json.dump(check_status_of_loop, json_file, sort_keys=True, indent=4)
        print("loop stopped")


# starts the loop in BootLoop file for sending message in channel.
@bot.command(name="start")
async def start_loop(ctx):
    if ctx.author.name == 'boco6969':
        with open(configuration.JSON_FILE) as json_file:
            check_status_of_loop = json.load(json_file)
        check_status_of_loop['stop_loop'] = False
        with open(configuration.JSON_FILE, 'w') as json_file:
            json.dump(check_status_of_loop, json_file, sort_keys=True, indent=4)
        print("loop start")


# Modifies the total_run in json file by adding the amount user provides
@bot.command(name="increment")
async def increment_count(ctx, increment_run):
    if ctx.author.name == 'boco6969':
        current_run = get_count()
        with open(configuration.JSON_FILE) as json_file:
            modify_run = json.load(json_file)
        modify_run['total_run'] = current_run + int(increment_run)
        with open(configuration.JSON_FILE, 'w') as json_file:
            json.dump(modify_run, json_file, sort_keys=True, indent=4)
        await ctx.send("@boco6969" + ' ' + "count added by " + increment_run + ". " + "Was: " + str(current_run)
                       + " Now: " + str(get_count()))


# Modifies the total_run in json file by adding the amount user provides
@bot.command(name="decrement")
async def decrement_count(ctx, decrement_run):
    if ctx.author.name == 'boco6969':
        current_run = get_count()
        with open(configuration.JSON_FILE) as json_file:
            modify_run = json.load(json_file)
        modify_run['total_run'] = current_run - int(decrement_run)
        with open(configuration.JSON_FILE, 'w') as json_file:
            json.dump(modify_run, json_file, sort_keys=True, indent=4)
        await ctx.send("@boco6969" + ' ' + "count subtracted by " + decrement_run + ". " + "Was: " + str(current_run)
                       + " Now: " + str(get_count()))


# Checks if the bot is connected to the chat
@bot.command(name="check")
async def check(ctx):
    print('here')
    await ctx.send("@" + ctx.author.name + " Im here")


# replies with discord link
@bot.command(name="discord")
async def send_discord(ctx):
    await ctx.send("@" + ctx.author.name + " https://discord.gg/dsWZdcWNhW")


# Gets the points for the users that used the points command with the prefix
@bot.command(name="points")
async def get_points(ctx):
    query = {'user': ctx.author.name}
    find_user = all_users.find_one(query)
    if find_user:
        send_points = find_user['points']
        await ctx.send("@" + ctx.author.name + " Your points: " + str(send_points))
    else:
        new_user = {
            'user': ctx.author.name,
            'points': '100'
        }
        all_users.insert_one(new_user)
        await ctx.send("@" + ctx.author.name + "." + " Your points: " + str(100))


# Rolls dice, 1-6. If it lands odd, point gets divided, even is multiplied
@bot.command(name="roll")
async def roll_dice(ctx, arg):
    query = {'user': ctx.author.name}
    find_user = all_users.find_one(query)
    if find_user:
        user_points = find_user['points']
        temporary_points = user_points  # Assigning original points to temp before I change the points
        random_roll = random.randint(1, 6)
        user_point_int = int(user_points)
        argument_int = int(arg)

        if user_point_int < argument_int:
            await ctx.send("@" + ctx.author.name + ". Your total point is: "
                           + user_points + ". " + "Insufficient points.")
        else:
            calculation = int(arg) * random_roll
            if random_roll % 2 == 1:
                user_points = int(user_points) + calculation
            else:
                user_points = int(user_points) - calculation
            if user_points < 0:
                user_points = 0
            new_points = {"$set": {"points": str(user_points)}}
            all_users.update_one(query, new_points)
        profit = int(user_points) - int(temporary_points)
        await ctx.send(
            "@" + ctx.author.name + " rolled dice " + str(random_roll) + "." + " Profit: " + str(profit) +
            "." + " Total points: " +
            str(user_points))
    else:
        await ctx.send("@" + ctx.author.name + "." + " You don't have points. Do !points to add points")


# Mod can add points to the users in chat
@bot.command(name="add")
async def addPoints(ctx, user_name, points):
    if ctx.author.name == 'boco6969':
        query = {'user': user_name}
        find_user = all_users.find_one(query)
        if find_user:
            user_points = find_user['points']
            add_points = int(user_points) + int(points)
            new_points = {"$set": {"points": str(add_points)}}
            all_users.update_one(query, new_points)
            await ctx.send("Added " + points + " points to " + "@" + user_name)
        else:
            await ctx.send(user_name + " is not in the database boss")
    else:
        await ctx.send("@" + ctx.author.name + " You are not Boco")


@bot.command(name='attempts')
async def sendRun_command(ctx):
    await ctx.send('@' + ctx.author.name + ' ' + str(get_count()))


# gets all the runs completed. Reads runs.json file and grabs all keys then adds them to run_list list
# def get_runs():
#     run_list = list(runs.distinct("run_name"))
#     with open('runs.json', 'r') as runs_json:
#         all_runs = json.loads(runs_json.read())
#     for key, value in all_runs.items():
#         run_list.append(key)
#     return run_list


# Gets all the runs from database and sends it to chat
@bot.command(name='runs')
async def runs(ctx):
    run_list = list(all_runs.distinct("run_name"))
    sorted_values = sorted(run_list, key=lambda x: all_runs.find_one({"run_name": x})["_id"], reverse=False)
    try:
        await ctx.send("Completed runs: " + str(', '.join(sorted_values)))

    except:
        print('error')


# Takes author name and message as argument then adds new object to the database using those arguments
@bot.command(name='addrun')
async def add_run_chat(ctx, *, run_name):
    query = {'run_name': run_name}
    find_run = all_runs.find_one(query)
    new_run = {
        'run_name': run_name,
        'added_by': ctx.author.name
    }
    if find_run:
        await ctx.send("@"+ctx.author.name + ' That run is already in the list')
    else:
        all_runs.insert_one(new_run)
        await ctx.send('@' + ctx.author.name + ' added ' + '*' + run_name + '*' + ' to the completed run list')


# Takes author message as argument then remove object from database
@bot.command(name='removerun')
async def remove_run_chat(ctx, *, run_name):
    filter_run = {'run_name': run_name}
    find_run = all_runs.find_one(filter_run)
    if find_run:
        all_runs.delete_one(filter_run)
        await ctx.send('@' + ctx.author.name + ' removed ' + '*' + run_name + '*' + ' from the completed run list')
    else:
        await ctx.send('@' + ctx.author.name + ' No such run in the list')


# Calls dadjoke api and sends it to the chat when command is called
@bot.command(name='dadjoke')
async def dad_joke(ctx):
    joke_url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "text/plain"}
    response = requests.get(joke_url, headers=headers)
    joke_text = response.text
    await ctx.send("@" + ctx.author.name + ' ' + joke_text)


@bot.command(name='list')
async def all_commands(ctx):
    await ctx.send('!dadjoke', '!discord', '!runs ',  '!addrun', '!removerun', '!points', '!fist', '!roll', '!check')


fist_list = ['Radagon', 'Maliketh', ' Radahn', 'Margit', 'Morgott', 'Mogh', 'Godfrey']


@bot.command(name='fist')
async def fist(ctx):
    await ctx.send("Fisted so far: " + str(', '.join(fist_list)))


@bot.command(name='wiki')
async def golan(ctx):
    await ctx.send("Yep. Its Golan and she VIP too")


@bot.command(name='whoisW')
async def jake(ctx):
    await ctx.send("Its Jake. W Jake")


if __name__ == '__main__':
    bot.run()
