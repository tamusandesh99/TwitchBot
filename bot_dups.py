import json
import random

import asyncio
import time
import aiohttp

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
all_quiz = my_database.quiz


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
    message = "Completed runs: " + str(', '.join(sorted_values))
    if len(message) <= 500:
        try:
            await ctx.send(message)
        except:
            print('Error')
    else:
        try:
            await ctx.send("Completed runs (part 1): " + str(', '.join(sorted_values[:len(sorted_values) // 2])))
            await ctx.send("Completed runs (part 2): " + str(', '.join(sorted_values[len(sorted_values) // 2:])))
        except:
            print('Error')


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


active_question = {
    "question": None,
    "answer": None,
    "asked_by": None
}
is_question_active = False


@bot.command(name='quiz')
async def quiz(ctx, *, user_answer=None):
    if user_answer is None:
        await send_question(ctx)
    else:
        await check_answer(ctx, user_answer)


async def send_question(ctx):
    global is_question_active

    if is_question_active:
        # Send the active question to the new user
        await ctx.send("Question: " + active_question["question"])
    else:
        try:
            question_data = all_quiz.find({"answered": False}, {"question": 1})
            all_questions = [data["question"] for data in question_data]
            if all_questions:
                random_question = random.choice(all_questions)
                quiz_answer_data = all_quiz.find_one({"question": random_question}, {"answer": 1})
                quiz_answer = quiz_answer_data["answer"]
                active_question["question"] = random_question
                active_question["answer"] = quiz_answer.lower().strip()
                active_question["asked_by"] = ctx.author.name
                is_question_active = True
                await ctx.send("Question: " + random_question + " *do !quiz answer* to answer")
            else:
                await ctx.send("No questions available at the moment.")
                # Here write a method to make all the questions in the database set to false.
        except Exception as e:
            await ctx.send("An error occurred while retrieving the question. Please try again later.")


# Checks if the answer is correct when the user answers
async def check_answer(ctx, user_answer):
    global is_question_active

    if not is_question_active:
        await ctx.send("No question is currently active.")
        return

    user_answer = user_answer.strip().lower()
    user_answer_words = user_answer.split()

    is_correct_answer = any(word in active_question["answer"] for word in user_answer_words)
    if is_correct_answer:
        await update_user_points(ctx.author.name, 10)
        await ctx.send("@" + ctx.author.name + " Correct answer! Added 10 points.")
        await mark_question_answered(active_question["question"])
    else:
        await ctx.send("@" + ctx.author.name + " Incorrect answer.")

    is_question_active = False
    active_question["question"] = None
    active_question["answer"] = None
    active_question["asked_by"] = None


@bot.event()
async def event_message(ctx):
    print(ctx.author.name)


# Update the user points from the database.
async def update_user_points(username, points_to_add):
    query_user = {'user': username}
    find_user = all_users.find_one(query_user)
    if find_user:
        user_points = find_user['points']
        add_points = int(user_points) + points_to_add
        new_points = {"$set": {"points": str(add_points)}}
        all_users.update_one(query_user, new_points)
    else:
        new_user = {
            'user': username,
            'points': '110'
        }
        all_users.insert_one(new_user)


#  Updates the status on database. If the question has been answered then it will not be repeated
async def mark_question_answered(question):
    set_question_as_answered = all_quiz.find_one({"question": question}, {"answered": 1})
    set_answered_true = {"$set": {"answered": True}}
    all_quiz.update_one(set_question_as_answered, set_answered_true)



# Calls dadjoke api and sends it to the chat when command is called
@bot.command(name='dadjoke')
async def dad_joke(ctx):
    joke_url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "text/plain"}
    response = requests.get(joke_url, headers=headers)
    joke_text = response.text
    await ctx.send("@" + ctx.author.name + ' ' + joke_text)


# Lists all the commands that is available
@bot.command(name='commands')
async def all_commands(ctx):
    await ctx.send('@' + ctx.author.name + ' ' + ' !dadjoke' + ' ' + ' !discord' + ' ' + ' !runs ' + ' ' + ' !addrun' +
                   ' ' + ' !removerun' + ' ' +
                   ' !points' + ' ' + ' !fist' + ' ' + ' !roll' + ' ' + ' !check')


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
