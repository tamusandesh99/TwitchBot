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


# gets run count from json file
def get_count():
    """ Reads the count from the JSON file and returns it """
    with open(config.JSON_FILE) as json_file:
        data = json.load(json_file)
        return data['total_run']


# turns the statement to false once a total run is sent to chat
def update_send_run():
    with open(config.JSON_FILE) as json_file:
        data = json.load(json_file)
        data['send_run'] = False
    with open(config.JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)


# checks if to send the total count to the streamers chat
def check_if_send_total_run():
    with open(config.JSON_FILE) as json_file:
        data = json.load(json_file)
        # print(data['send_run'])
        return data['send_run']


def stop_loop():
    with open(config.JSON_FILE) as json_file:
        check_status_of_loop = json.load(json_file)
        # print(data['send_run'])
        return check_status_of_loop['stop_loop']


@bot.event()
async def event_ready():
    print('Bot is ready with run of: ' + str(get_count()))


# this runs in infinite loop. Checks weather to send the run count on chat or not from json file """
@bot.event()
async def event_ready():
    while True:
        if not stop_loop():
            print("bot is running")
            if check_if_send_total_run():
                print('--------------------------')
                print("Sending total count now: " + str(get_count()))
                print('--------------------------')
                # time.sleep(3)
                await bot.connected_channels[0].send('Total run: ' + str(get_count()))
                update_send_run()
        else:
            print("bot has stopped")
        time.sleep(3)


if __name__ == '__main__':
    bot.run()
