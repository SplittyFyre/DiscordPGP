from curses import *
import var
import asyncio
import discord_listen
import threading

var.init()

loop = asyncio.get_event_loop()
loop.create_task(discord_listen.go())
t = threading.Thread(target=loop.run_forever)
t.start()



stdscr = initscr()

sizey, sizex = stdscr.getmaxyx()

chat = newwin(sizey - 2, sizex, 0, 0)
textbox = newwin(2, sizex, sizey - 2, 0)
stdscr.refresh()

noecho()
stdscr.timeout(1)
chat.scrollok(True)

chat.addstr('You may now chat:\n')
chat.refresh()

s = ''

while True:

    var.inbuf_mutex.acquire()
    for m in var.inbuf:
        chat.addstr(m + '\n')
    var.inbuf.clear()
    var.inbuf_mutex.release()

    c = stdscr.getch()
    if c == ERR:
        chat.refresh() # for ^
        continue

    if c == KEY_BACKSPACE or c == KEY_DC or c == 127:
        if s:
            s = s[:-1]
    else:
        if c == ord('\n'):

            if s == '/exit':
                break

            chat.addstr(s + '\n')
            var.outbuf_mutex.acquire()
            var.outbuf.append(s)
            var.outbuf_mutex.release()
            s = ''
        else:
            s += chr(c)

    textbox.clear()
    textbox.addstr('>>> ' + s)

    textbox.refresh()
    chat.refresh()


chat.addstr("Stopping event loop...\n")
chat.refresh()
loop.stop()

chat.addstr("Joining thread... (this may take some time)\n")
chat.refresh()
t.join()

endwin()