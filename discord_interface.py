import discord
import asyncio
import var

client = discord.Client()

@client.event
async def on_ready():
    var.inbuf_mutex.acquire()
    var.inbuf.append('Logged in as {0.user}'.format(client))
    var.inbuf_mutex.release()

@client.event
async def on_message(message):
    if message.author == client.user or message.channel != var.destination:
        return
    var.inbuf_mutex.acquire()
    var.inbuf.append(message.content)
    var.inbuf_mutex.release()


async def send_task():
    await client.wait_until_ready()
    while not client.is_closed():
        var.outbuf_mutex.acquire()
        for m in var.outbuf:
            await var.destination.send(m)
        var.outbuf.clear()
        var.outbuf_mutex.release()
        await asyncio.sleep(0.001)

def getChannel(chanid):
    return client.get_channel(chanid)

client.loop.create_task(send_task())

async def go():
    await client.start("NTI4MjYwMTg3NDM4NzEwODI0.X7COuQ.qwPYB3FBD3B87TKk8c-WD9ohtV4", bot=False)

