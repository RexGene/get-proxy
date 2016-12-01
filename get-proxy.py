import optparse
import re
import urllib2
import socks
import socket
import sys


if __name__ == "__main__":
    sys.stderr.write("\033[1;31;40m")
    parse = optparse.OptionParser('usage: %prog -f [format] -t [timeout]')
    parse.add_option('-f', dest='fmt', type='string')
    parse.add_option('-t', dest='timeout', type='int')

    options, _ = parse.parse_args()
    if options.fmt == None:
        options.fmt = "%s\t%s\t%s"

    if options.timeout == None:
        options.timeout = 5

    regex = re.compile('<tr>\s+<td>\d+</td>\s+<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>\s+<td>(\d+)</td>\s+<td>.+</td>\s+<td><a.+>(.+)</a></td>[\s\S]+?</tr>', re.M)

    resultList = []
    try:
        resp = urllib2.urlopen('http://31f.cn/socks5-proxy/', timeout=options.timeout)
    except Exception, msg:
        sys.stderr.write("get socks list error:%s\n" % (msg))

    result = regex.findall(resp.read())

    for ip, port, type in result:
        t = 0
        if type == 'socks4':
            t = socks.SOCKS4
        elif type == 'socks5':
            t = socks.SOCKS5
        else:
            sys.stderr.write("unknow socks type\n" % (type))
            continue

        socks.setdefaultproxy(t, ip, int(port))
        socket.socket = socks.socksocket 
        try:
            ipStr = urllib2.urlopen('http://icanhazip.com', timeout=options.timeout)

            if ip == ipStr.read().strip():
                resultList.append((ip, port, type))
        except Exception, msg:
            sys.stderr.write("ip:%s msg:%s\n" % (ip, msg))

    for ip, port, type in resultList:
        print options.fmt %(type,ip,port)

    sys.stderr.write("\033[0m")
