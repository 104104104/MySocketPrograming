# -*- coding: utf-8 -*-
import socket, threading

def reception_handler(soc):
    while True:
        data = soc.recv(1024)
        print()
        print("メッセージを受信しました！")
        print("[受信]{}".format(data.decode("utf-8")))

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip="localhost"
    port = 50007
    soc.connect((ip, port))

    name=input('input_your_name >>')
    #soc.send(name.encode())

    recp_thread = threading.Thread(target=reception_handler, args=(soc,), daemon=True)
    recp_thread.start()

    while 1:
        #to_name = input("to_name >> ")
        print(name, "さん")
        send_message = input("send_message >> ")
        data=[name, send_message]
        data = str(data).encode()   # バイナリに変換
        soc.send(data)              # ソケットに入力したデータを送信

if __name__ == '__main__':
    main()
