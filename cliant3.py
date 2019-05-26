# -*- coding: utf-8 -*-
import socket

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip="localhost"
    port = 50007
    soc.connect((ip, port))

    while 1:
        data = input("send_message >> ")
        data = str(data).encode()   # バイナリに変換
        soc.send(data)              # ソケットに入力したデータを送信
        # ソケットから指定したバッファバイト数だけデータを受け取る
        message = soc.recv(1024)
        print('Recv_message >> ', message.decode())

if __name__ == '__main__':
    main()
