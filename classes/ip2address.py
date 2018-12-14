def ip2long(ip):
    ip_list = ip.split('.')
    result = 0
    for i in range(4):  # 0,1,2,3
        result = result + int(ip_list[i]) * 256 ** (3 - i)
    return result


# transfer int to ip
def long2ip(long):
    floor_list = []
    yushu = long
    for i in reversed(range(4)):  # 3,2,1,0
        res = divmod(yushu, 256 ** i)
        floor_list.append(str(res[0]))
        yushu = res[1]
    return '.'.join(floor_list)
