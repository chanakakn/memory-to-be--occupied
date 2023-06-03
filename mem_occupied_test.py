#!/usr/bin/env python
import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def find_memto_occupy(pc):
    if pc > 100:
        raise ValueError("Wrong percentage given: %d" % pc)

    with open('/proc/meminfo', 'r') as meminfo:
        for line in meminfo:
            if line.startswith('MemTotal:'):
                mem = int(line.split()[1])
                break
        else:
            raise RuntimeError("Unable to find the available memory")

    mem = (mem / 100) * pc
    return int(mem / 1024)

def occupy_memory(mb):
    b = mb * 1024 * 1024

    memfile = bytearray(b)
    memfile[-1] = 0

    input("%d MB memory is occupied, press ENTER to release: " % mb)
    del memfile

    print("Memory released")

if __name__ == "__main__":
    try:
        num = sys.argv[1] if len(sys.argv) > 1 else None
        if not num or not num.isdigit() or int(num) < 1:
            print("Usage: %s <occupy MB>\nEx: %s 100 - occupies 100 MB memory" % (sys.argv[0], sys.argv[0]))
            sys.exit(1)

        if num.endswith('%'):
            pc = int(num[:-1])
            mb = find_memto_occupy(pc)
        else:
            mb = int(num)

        occupy_memory(mb)

    except ValueError as ve:
        logger.error(str(ve))
    except FileNotFoundError as fnf:
        logger.error("Unable to open /proc/meminfo to find available memory")
    except Exception as e:
        logger.exception("An error occurred: %s", str(e))
