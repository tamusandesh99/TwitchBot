import random
import asyncio
import configuration
import requests
import time
import extraCommands

from twitchio.ext import commands
from pymongo.mongo_client import MongoClient


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


@bot.event()
async def event_ready():
    print(f"Connected to {configuration.CHANNEL}")


# Event triggered when Twitch sends a RECONNECT notice
@bot.event
async def event_reconnect():
    print("Received a RECONNECT notice. Reconnecting...")


@bot.event()
async def event_message(ctx):
    try:
        query_user = {'user': ctx.author.name}
        find_user = await all_users.find_one(query_user)
        if find_user:
            user_points = find_user.get('points', 0)
            add_points = int(user_points) + 1
            new_points = {"$set": {"points": str(add_points)}}
            all_users.update_one(query_user, new_points)
        else:
            new_user = {
                'user': ctx.author.name,
                'points': '15'
            }
            all_users.insert_one(new_user)

            time.sleep(3)

    except Exception as e:
        print(f"An error occurred in event_message: {str(e)}")


# Checks if the bot is connected to the chat
@bot.command(name="check")
async def check(ctx):
    print('here')
    await ctx.send("@" + ctx.author.name + " You are checked in")


# replies with discord link
@bot.command(name="discord")
async def send_discord(ctx):
    await ctx.send("@" + ctx.author.name + " https://discord.gg/dsWZdcWNhW")


# Calls dadjoke api and sends it to the chat when command is called
@bot.command(name='dadjoke')
async def dad_joke(ctx):
    try:
        joke_url = "https://icanhazdadjoke.com/"
        headers = {"Accept": "text/plain"}
        response = requests.get(joke_url, headers=headers)
        response.raise_for_status()  # Raises an exception if the request was not successful
        joke_text = response.text
        await ctx.send("@" + ctx.author.name + ' ' + joke_text)
    except requests.RequestException as e:
        # Handle any request-related exceptions here
        print("An error occurred during the request:", str(e))
        await ctx.send("Mind is running blank at the moment")
    except Exception as e:
        # Handle any other exceptions that may occur
        print("An unexpected error occurred:", str(e))


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
        await ctx.send("@" + ctx.author.name + " do !addrun to add run names")


# Gets all the runs from database and sends it to chat
@bot.command(name='runs')
async def runs(ctx):
    run_list = list(all_runs.distinct("run_name", {"$or": [{"game_name": ""}, {"game_name": {"$exists": False}}]}))
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


@bot.command(name='runsds')
async def runs(ctx):
    run_list = list(all_runs.distinct("run_name", {"game_name": "DS3"}))
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
        await ctx.send("@" + ctx.author.name + ' That run is already in the list')
    else:
        all_runs.insert_one(new_run)
        await ctx.send('@' + ctx.author.name + ' added ' + '*' + run_name + '*' + ' to the completed run list')


@bot.command(name='addrunds')
async def add_run_chat(ctx, *, run_name):
    query = {'run_name': run_name}
    find_run = all_runs.find_one(query)
    new_run = {
        'run_name': run_name,
        'added_by': ctx.author.name,
        'game_name': 'DS3'
    }
    if find_run:
        await ctx.send("@" + ctx.author.name + ' That run is already in the list')
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
        await ctx.send("Question: " + active_question["question"] + "asked by " + active_question["asked_by"])
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


# Lists all the commands that is available
@bot.command(name='commands')
async def all_commands(ctx):
    await ctx.send('@' + ctx.author.name + ' ' + extraCommands.all_commands())


@bot.command(name='fist')
async def fist(ctx):
    await ctx.send("Fisted so far: " + extraCommands.fist())


@bot.command(name='golan')
async def golan(ctx):
    await ctx.send(extraCommands.golan())


@bot.command(name='whoisW')
async def jake(ctx):
    await ctx.send(extraCommands.jake())


RECONNECT_DELAY = 2000  # Delay in seconds between reconnection attempts
MAX_RECONNECT_ATTEMPTS = 50  # Maximum number of reconnection attempts


# To reconnect to the channel if it fails midway
def reconnect_bot():
    reconnect_attempt = 0
    while reconnect_attempt < MAX_RECONNECT_ATTEMPTS:
        try:
            print("Reconnecting...")
            bot.run()
        except Exception as e:
            print(f"Reconnection attempt {reconnect_attempt + 1} failed.")
            print(f"Error: {e}")
            reconnect_attempt += 1
            time.sleep(RECONNECT_DELAY)
    print(f"Max reconnection attempts reached. Exiting...")


if __name__ == '__main__':
    reconnect_bot()
    # bot.run()
