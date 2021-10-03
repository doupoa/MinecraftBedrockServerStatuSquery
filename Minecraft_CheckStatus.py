from socket import *
import os
import time
import uuid


def GetData(BE_HOST: str, BE_PORT: int):
    BE_IP = gethostbyname(BE_HOST)
    # 执行查询指令
    # 此处进行编码转换 base64 -> utf-8
    addr = (BE_IP, BE_PORT)  # 定义目标地址及端口
    # 生成GUID，在C++中此值称为GUID，在Python中却叫UUID
    UUID = str(uuid.uuid1()).upper().split("-")
    TIME = int((time.perf_counter())*10000000)  # 获取程序已启动时间，精准至小数后5位
    tickcounttime = '%016d' % TIME  # 将启动时间填充零至16字节
    STR = "01"+str(tickcounttime) + \
        "00FFFF00FEFEFEFEFDFDFDFD12345678" + UUID[2]+UUID[4]  # 缝合数据包
    STR1 = bytes.fromhex(STR)  # 将数据包转换为16进制
    try:  # 尝试连接
        # 定义socket为UDP 内部大写字符为socket的特征码，详情请查阅相关资料
        UDPC = socket(AF_INET, SOCK_DGRAM)
        socket.settimeout(UDPC, 5)  # 设置超时时间为5秒
        socket.connect(UDPC, addr)  # 连接远程地址
        UDPC.sendto(STR1, addr)  # 发送数据包
        rec = socket.recvfrom(UDPC, 1024)  # 设置接收缓冲区
        Cleaning = str(rec).split(';')
        return '基岩版服务器查询信息:\n服务器名:{}\n玩家:{}/{}\n游戏版本:{}\n游戏模式:{}\n存档名:{}'.format(
            Cleaning[1], Cleaning[4], Cleaning[5], Cleaning[3], Cleaning[8], Cleaning[7])
    except:
        return BE_HOST + "上的服务器离线"


if __name__ == '__main__':
    host = input('请键入基岩服务端域名/IP：')
    port = input('请键入基岩服务端端口:')
    if host and port:
        print("\n"+GetData(host, int(port))+"\n")
        os.system('pause')
    else:
        print('参数错误')
        os.system('pause')
