from twitchio.ext import commands
import config
import mss
import mss.tools
import time
from PIL import Image
from pytesseract import pytesseract
total_death = 51

bot = commands.Bot(
    token=config.TMI_TOKEN,
    client_id=config.CLIENT_ID,
    nick=config.BOT_NICK,
    prefix=config.BOT_PREFIX,
    initial_channels=[config.CHANNEL],
)


@bot.event()
async def event_message(ctx):
    print(ctx.author)
    print(ctx.content)
    await bot.handle_commands(ctx)


@bot.event()
async def sendRunCount(run: int):
    ws = bot._ws
    await ws.send_privsgm


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


def main():
    global total_death
    myconfig = r"--psm 3 --oem 3"
    with mss.mss() as sct:
        while True:
            monitor_number = 1
            mon = sct.monitors[monitor_number]

            # The screen part to capture
            monitor_died = {
                "top": mon["top"] + 410,  # 100px from the top
                "left": mon["left"] + 550,  # 100px from the left
                "width": 450,
                "height": 160,
                "mon": monitor_number,
            }
            monitor_blade = {
                "top": mon["top"] + 710,  # 100px from the top
                "left": mon["left"] + 550,  # 100px from the left
                "width": 450,
                "height": 110,
                "mon": monitor_number,
            }
            output_died = "./screenshots/died.png".format(**monitor_died)
            output_blade = "./screenshots/blade.png".format(**monitor_died)

            # Grab the data
            sct_img_died = sct.grab(monitor_died)
            sct_img_blade = sct.grab(monitor_blade)

            # Save to the picture file
            mss.tools.to_png(sct_img_died.rgb, sct_img_died.size, output=output_died)
            mss.tools.to_png(sct_img_blade.rgb, sct_img_blade.size, output=output_blade)

            text_died = pytesseract.image_to_string('./screenshots/died.png', config=myconfig)
            text_blade = pytesseract.image_to_string('./screenshots/blade.png', config=myconfig)

            print(text_died)
            print(text_blade)
            if 'Malenia' in text_blade or 'Blade' in text_blade or 'Miquella' in text_blade:
                print("Blade")
                total_death += 1
                time.sleep(5)
            if 'YOU' in text_died or 'DIED' in text_died:
                print('Died')
                total_death += 1
                time.sleep(5)
            print(total_death)


if __name__ == '__main__':
    # main()
    bot.run()
