from curses import *
import var
import asyncio
import discord_interface
import crypto
import threading

var.init()

loop = asyncio.get_event_loop()
loop.create_task(discord_interface.go())
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

def parseCommand(cmd):
    if cmd[0] == '/channel':
        if len(cmd) != 2:
            chat.addstr("/channel: wrong number of arguments\n")
            return

        if not cmd[1].isdigit():
            chat.addstr('Error: invalid integer value\n')
            return

        var.outbuf_mutex.acquire()
        var.destination = discord_interface.getChannel(int(cmd[1]))
        var.outbuf_mutex.release()

        if var.destination is None:
            chat.addstr('Error: invalid channel\n')
        else:
            chat.addstr('Joined channel id ' + cmd[1] + '\n')

    elif cmd[0] == '/gpg':
        if len(cmd) >= 2:
            if cmd[1] == 'list':
                keys = crypto.gpg.list_keys()
                for i in keys:
                    chat.addstr('{}\t\t{}\n'.format(i['uids'][0], i['keyid']))
            elif cmd[1] == 'recipient':
                if len(cmd) != 3:
                    chat.addstr('You need to specify a key id (try /gpg list)\n');
                    return
                crypto.recipient = cmd[2]
                chat.addstr('GPG recipient now set to ' + crypto.recipient)
        else:
            chat.addstr('/gpg: list, recipient\n')

    else:
        chat.addstr('Invalid command: {}\n'.format(cmd[0]))


def canSend():
    if var.destination is None:
        chat.addstr('Send error: destination is undefined\n')
        return False
    if crypto.recipient is None:
        chat.addstr('Send error: gpg recipient is undefined\n')
        return False
    return True


while True:
    var.inbuf_mutex.acquire()
    for m in var.inbuf:
        chat.addstr(m + '\n')
    var.inbuf.clear()
    var.inbuf_mutex.release()

    c = stdscr.getch()

    if c == KEY_BACKSPACE or c == KEY_DC or c == 127:
        if s: s = s[:-1]
    elif c != ERR:
        if c == ord('\n'):
            if s:
                if s[0] == '/':
                    if s == '/exit': break;
                    else: parseCommand(s.split(' '))
                else:
                    if canSend():
                        chat.addstr(s + '\n')
                        good, cipher = crypto.encrypt(s)
                        if good:
                            var.outbuf_mutex.acquire()
                            var.outbuf.append(cipher)
                            var.outbuf_mutex.release()
                        else:
                            chat.addstr('GPG encryption failure: ' + cipher)
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