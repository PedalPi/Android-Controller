#!/usr/bin/python
# accessory.py
# License GPLv2
# (c) Manuel Di Cerbo, Nexus-Computing GmbH
# https://github.com/rosterloh/pyusb-android/blob/master/accessory.py
import os
import socket


NETLINK_KOBJECT_UEVENT = 15


def main():
    while True:
        sock = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, NETLINK_KOBJECT_UEVENT)
        sock.bind((os.getpid(), -1))

        while True:
            data = sock.recv(512)
            vid = parse_uevent(data)
            if vid is not None:
                break

        sock.close()
        accessory_task(vid)


def parse_uevent(data):
    """
    :param bytes data:
    :return:
    """

    lines = data.decode('UTF8', 'ignore').split('\0')

    #lines = data.decode('UTF8').split('\0')#.replace('\fe', b'').decode('UTF8')
    print(lines)
    keys = []
    for line in lines:
        val = line.split('=')
        if len(val) == 2:
            keys.append((val[0], val[1]))

    attributes = dict(keys)
    if 'ACTION' in attributes and 'PRODUCT' in attributes:
        if attributes['ACTION'] == 'add':
            parts = attributes['PRODUCT'].split('/')
            return int(parts[0], 16)

    return None

def accessory_task(teste):
    print(teste)

if __name__ == '__main__':
    main()