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
    var.inbuf_mutex.acquire()
    var.inbuf.append(message.content)
    var.inbuf_mutex.release()


async def send_task():
    await client.wait_until_ready()
    recv = client.get_channel(777038663401865250)
    while not client.is_closed():
        var.outbuf_mutex.acquire()
        for m in var.outbuf:
            await recv.send(m)
        var.outbuf.clear()
        var.outbuf_mutex.release()
        await asyncio.sleep(0.001)


client.loop.create_task(send_task())

async def go():
    await client.start("NTI4MjYwMTg3NDM4NzEwODI0.X5hrUg.0kdfwIF3g2TV0s3xvYqiPf1sGjQ", bot=False)

