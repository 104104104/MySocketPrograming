# -*- coding: utf-8 -*-
import socket, threading
from datetime import datetime
def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip="localhost"
    port = 50000
    soc.connect((ip, port))

    name=input('input_your_name >>')
    print()

    while 1:
        print(name, "さん")
        mode=input("i: send_sessage, b: check_board, d: direct_message, q: quit >> ")
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

        elif mode=="q":
            break
        else:
            print("Error!")
            pass

if __name__ == '__main__':
    main()
