import discord
import asyncio
import threading

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

async def my_background_task():
    await client.wait_until_ready()
    recv = client.get_channel(777038663401865250)
    while not client.is_closed():
        await recv.send('I am sorry for the large volume')
        print('sent')
        await asyncio.sleep(5)

client.loop.create_task(my_background_task())


loop = asyncio.get_event_loop()
loop.create_task(client.start("NTI4MjYwMTg3NDM4NzEwODI0.X5hrUg.0kdfwIF3g2TV0s3xvYqiPf1sGjQ", bot=False))

t = threading.Thread(target=loop.run_forever)
t.start()

print('started')
input()

print('trying to stop:')
loop.stop()
print('joining:')
t.join()

