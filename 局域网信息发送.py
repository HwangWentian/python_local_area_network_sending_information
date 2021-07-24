import socket as skt
import threading as td
from base64 import b64encode as b64en, b64decode as b64de


def find_port():
    ip_fp = skt.gethostbyname_ex(skt.gethostname())[2][0]
    port_fp = 1024
    while True:
        try:  # 尝试绑定端口，如果成功则返回 IP、端口和套接字对象
            sk_fp = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
            sk_fp.bind((ip_fp, port_fp))
            return [ip_fp, port_fp, sk_fp]
        except OSError:
            port_fp += 1


def listen(sk_listen_p: skt.socket):
    while True:
        sk_listen_p.listen()
        conn_p, adr_p = sk_listen_p.accept()
        adr_p = "（%s: %s）" % (adr_p[0], adr_p[1])
        record = "\n来自 %s 的消息：%s\n" % (adr_p, b64de(conn_p.recv(1000)).decode("utf-8"))
        print(record)

        write_record(record)


def send(sk_send_p: skt.socket, ip_p: str, port_p: int):
    sk_send_p.connect((ip_p, port_p))
    while True:
        message = b64en(input("请输入信息：").encode("utf-8")).decode("utf-8")
        sk_send_p.sendall(message.encode("utf-8"))

        adr_p = "（%s: %s）" % (ip_p, port_p)
        record = "\n来自 %s （本机）的消息：%s\n" % (adr_p, b64de(message.encode("utf-8")).decode("utf-8"))
        write_record(record)


def write_record(information):
    with open("records.txt", "wb+") as file_obj:
        file_obj.write(file_obj.read() + information.encode("utf-8"))


if __name__ == "__main__":
    IP, Port, sk_listen = find_port()

    print("你的地址是：%s\n连接端口是：%s\n" % (IP, Port))
    print("你想连接到哪台主机？在该主机上运行这个程序，然后输入显示的信息以连接")

    td.Thread(target=listen, args=(sk_listen,), name="Listen").start()

    while True:
        adr_c = input("输入地址：")
        try:
            td.Thread(target=send, args=(skt.socket(skt.AF_INET, skt.SOCK_STREAM),
                                         adr_c, int(input("输入端口："))), name="Send").start()
            break
        except ValueError:
            print("请重新输入！")
            continue
