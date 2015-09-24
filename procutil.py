import os
import os.path
import re
import socket
import struct

from collections import defaultdict

def inode_table() :
    """
        returns table of inodes to PID
    """

    inode_table = defaultdict(list)

    for pid in os.listdir('/proc') :
        if pid.isdigit() :
            for fd in os.listdir('/proc/' + pid + '/fd') :
                try :
                    sl = os.readlink('/proc/' + pid + '/fd/' + fd)
                    match = re.compile(r'socket:\[(\d+)\]$').match(sl)
                    if match :
                        inode = match.group(1)
                        inode_table[inode].append(pid)
                except OSError :
                    pass

    return inode_table

def decode_address(addr) :
    """
        Convert IP/Port pair obtained in /proc/net/<family> entry to human readable.
        accepts hexadecimal encoded string containing IP address and port seperated
        a semicolon. (XXXXXXXX:YYYY)

        returns ip as dotted decimal and port as long
    """

    ip_port = addr.split(":")

    ip_long = int(ip_port[0], 16)
    port_long = int(ip_port[1], 16)

    ip_ascii = socket.inet_ntoa(struct.pack("<L", ip_long))

    return (ip_ascii, port_long)

def connections() :
    """
        returns list of processes with the local and remote connections
    """
    proc_tcp = open('/proc/net/tcp')

    lines = [p for p in proc_tcp]

    headers = lines[0].split()
    #print headers
    headers[4:6] = ['_'.join(headers[4:6])]
    headers[5:7] = ['_'.join(headers[5:7])]

    # map of column name to position
    h = {}

    for x in xrange(len(headers)) :
        h[headers[x]] = x


    entries = [line.split() for line in lines[1:]]

    inodes = inode_table()
    retval = []

    for entry in entries :

        local =  entry[h['local_address']]
        remote = entry[h['rem_address']]
        inode = entry[h['inode']]

        local_address =  decode_address(local)
        remote_address = decode_address(remote)
        if inodes[inode]:
            pid = inodes[inode][0]
            if os.path.isfile('/proc/' + pid + '/comm'):
                proc_name  = open('/proc/' + pid + '/comm').read().rstrip()
            else:
                statfile = open('/proc/' + pid + '/stat')
                try:
                    proc_name = statfile.readline().rstrip().split()[1].strip('()')
                finally:
                    statfile.close()
            if not proc_name:
                proc_name = ''
            retval.append({'proc' : proc_name, 'local' : local_address, 'remote' : remote_address})

    return retval
