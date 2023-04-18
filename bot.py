import json
from twitchio.ext import commands
import configuration
import random


""" Initializing the bot """
bot = commands.Bot(
    token=configuration.TMI_TOKEN,
    client_id=configuration.CLIENT_ID,
    nick=configuration.BOT_NICK,
    prefix=configuration.BOT_PREFIX,
    initial_channels=[configuration.CHANNEL],
)


# gets run count from json file
def get_count():
    """ Reads the count from the JSON file and returns it """
    with open(configuration.JSON_FILE) as json_file:
        data = json.load(json_file)
        return data['total_run']

# @bot.event()
# async def event_message(ctx):
#     try:
#         print(ctx.author.name + ": " + ctx.content)
#     except:
#         await bot.handle_commands(ctx)


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


# Returns the rules for roll commands
@bot.command(name="rules")
async def rules(ctx):
    await ctx.send("Rules are simple: if you roll odd, your points get divided. If even then multiplied" )


# Mod can add points to the users in chat
@bot.command(name="add")
async def addPoints(ctx, user_name, points):
    if ctx.author.name == 'boco6969':
        with open(configuration.POINTS_FILE) as json_file:
            users_data = json.load(json_file)
        if user_name in users_data:
            add_points = int(users_data[user_name]) + int(points)
            users_data[user_name] = add_points
            with open(configuration.POINTS_FILE, 'w') as json_file:
                json.dump(users_data, json_file, sort_keys=True, indent=4, separators=(',', ': '))
            await ctx.send("Added " + points + " points to " + "@" + user_name)
        else:
            await ctx.send(user_name + " is not in the database boss")
    else:
        await ctx.send("@" + ctx.author.name + " You are not Boco")


# Checks if the bot is connected to the chat
@bot.command(name="check")
async def check(ctx):
    print('here')
    await ctx.send("@" + ctx.author.name + " Im here")


# replies with discord link
@bot.command(name="discord")
async def send_discord(ctx):
    print('here')
    await ctx.send("@" + ctx.author.name + " https://discord.gg/dsWZdcWNhW")


# Gets the points for the users that used the points command with the prefix
@bot.command(name="points")
async def get_points(ctx):
    with open(configuration.POINTS_FILE) as json_file:
        users_data = json.load(json_file)
    if ctx.author.name in users_data:
        print(users_data[ctx.author.name])
        send_points = int(users_data[ctx.author.name])
        await ctx.send("@" + ctx.author.name + " Your points: " + str(send_points))
    else:
        users_data[ctx.author.name] = 30
        with open(configuration.POINTS_FILE, 'w') as json_file:
            json.dump(users_data, json_file, sort_keys=True, indent=4, separators=(',', ': '))
        await ctx.send("@" + ctx.author.name + "." + " Your points: " + str(30))


# Rolls dice, 1-6. If it lands odd, point gets divided, even is multiplied
@bot.command(name="roll")
async def roll_dice(ctx, arg):
    with open(configuration.POINTS_FILE) as json_file:
        users_data = json.load(json_file)
    if ctx.author.name in users_data:
        user_point = users_data[ctx.author.name]
        temporary_points = user_point  # Assigning original points to temp before I change the points
        random_roll = random.randint(1, 6)
        user_point_int = int(user_point)
        argument_int = int(arg)

        if user_point_int < argument_int:
            await ctx.send("@" + ctx.author.name + ". Your total point is: "
                           + str(int(user_point)) + ". " + "Insufficient points.")
        else:
            calculation = int(arg) * random_roll
            if random_roll % 2 == 1:
                user_point = user_point + calculation
            else:
                user_point = user_point - calculation
            if user_point < 0:
                user_point = 0
            users_data[ctx.author.name] = user_point
        with open(configuration.POINTS_FILE, 'w') as json_file:
            json.dump(users_data, json_file, sort_keys=True, indent=4, separators=(',', ': '))
        profit = user_point - temporary_points
        await ctx.send(
            "@" + ctx.author.name + " rolled dice " + str(random_roll) + "." + " Profit: " + str(int(profit)) +
            "." + " Total points: " +
            str(int(users_data[ctx.author.name])))
    else:
        await ctx.send("@" + ctx.author.name + "." + " You don't have points. Do !points to add points")


@bot.command(name='attempts')
async def sendRun_command(ctx):
    await ctx.send('@' + ctx.author.name + ' ' + str(get_count()))


# gets all the runs completed. Reads runs.json file and grabs all keys then adds them to run_list list
def get_runs():
    run_list = []
    with open('runs.json', 'r') as runs_json:
        all_runs = json.loads(runs_json.read())
    for key, value in all_runs.items():
        run_list.append(key)
    return run_list


# Calls get_runs method then sends all the runs to the chat
@bot.command(name='runs')
async def runs(ctx):
    run_list = get_runs()
    try:
        await ctx.send("Completed runs: " + str(', '.join(run_list)))

    except:
        print('error')


# Takes the run name and the person who added as an argument then adds them to json file
def add_run_json(run_name, author):
    with open('runs.json', 'r') as runs_json:
        all_runs = json.loads(runs_json.read())
    all_runs[run_name] = author
    with open('runs.json', 'w') as runs_json:
        runs_json.write(json.dumps(all_runs, indent=4))


# Takes the run name as an argument then removes it from the json file
def remove_run_json(run_name):
    with open('runs.json', 'r') as runs_json:
        all_runs = json.loads(runs_json.read())
        del all_runs[run_name]
    with open('runs.json', 'w') as runs_json:
        runs_json.write(json.dumps(all_runs, indent=4))


# Takes author name and message as argument then calls add_run_json method using those arguments
@bot.command(name='addrun')
async def add_run_chat(ctx, *, run_name):
    add_run_json(run_name, ctx.author.name)
    await ctx.send('@' + ctx.author.name + ' added ' + '*' + run_name + '*' + ' to the completed run list')


# Takes author message as argument then calls remove_run_json method using those arguments
@bot.command(name='removerun')
async def remove_run_chat(ctx, *, run_name):
    remove_run_json(run_name)
    await ctx.send('@' + ctx.author.name + ' removed ' + '*' + run_name + '*' + ' from the completed run list')


fist_list = ['Radagon the Golden Order', 'Maliketh the black blade', 'Starscourage Radahn', 'Margit the Fell Omen', 'Morgott the Omen King', 'Mogh the Omen', 'Godfrey First Elden Lord']


@bot.command(name='fist')
async def fist(ctx):
    await ctx.send("Fisted so far: " + str(', '.join(fist_list)))


@bot.command(name='streamMind')
async def golan(ctx):
    await ctx.send("Yep. Its Golan and she VIP too")


@bot.command(name='whoisW')
async def jake(ctx):
    await ctx.send("Its Jake. W Jake")


if __name__ == '__main__':
    bot.run()
