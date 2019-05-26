# -*- coding: utf-8 -*-
import socket, threading
from datetime import datetime

def direct_handler(soc):
    while 1:
        data = soc.recv(1024)
        print()
        print("メッセージを受信しました！")
        print("[受信]{}".format(data.decode("utf-8")))

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip="localhost"
    port = 50000
    soc.connect((ip, port))
    num=int(soc.recv(1024).encode())

    dsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dip="localhost"
    dport = 50000+num
    dsoc.connect((dip, dport))

    name=input('input_your_name >>')
    soc.send(name.encode())
    print()

    direct_thread = threading.Thread(target=direct_handler, args=(dsoc,), daemon=True)
    direct_thread.start()

    while 1:
        print(name, "さん")
        mode=input("i: send_sessage, b: check_board, q: quit >> ")
        print()
        soc.send(mode.encode())
        if mode=="i":
            message = input("send_message >> ")
            print()
            send_message=message
            data=["("+datetime.now().strftime("%Y/%m/%d %H:%M:%S")+")"+name, send_message]
            data = str(data).encode()
            soc.send(data)
        elif mode=="b":
            print("\n--------------------------------------\n")
            board = soc.recv(1024).decode()
            flip=1
            for i in board:
                if flip and i=="\n":
                    print(" さんのメッセージ", end="")
                    flip=0
                elif not flip and i=="\n":
                    flip=1
                    print()
                print(i, end="")

            print("\n--------------------------------------\n")
        elif mode=="d":
            to_name=input("to_name >> ")
            message=input("send_message >> ")
            data=["("+datetime.now().strftime("%Y/%m/%d %H:%M:%S")+")"+name,  to_name, message]
            data=str(data).encode()
            soc.send(data)
        elif mode=="q":
            break
        else:
            print("Error!")
            pass

if __name__ == '__main__':
    main()
