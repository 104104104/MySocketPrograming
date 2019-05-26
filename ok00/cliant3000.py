# -*- coding: utf-8 -*-
import socket, threading
from datetime import datetime
from time import sleep

def reception_handler(soc):
    sleep(0.05)
    while True:
        data = soc.recv(1024).decode()
        if data[0]=="#" and data[1]=="#" and data[2]=="#":#初めの三文字が#であれば、ダイレクトメッセージ。適宜名前とメッセージに分解する。
            print()
            print("ダイレクトメッセージを受信しました！")
            f=0
            c=0
            for i in range(3, len(data)-1):
                if data[i]!="#":
                    print(data[i], end="")
                elif c>=3:
                    print(data[i], end="")
                elif not f:
                    print(" さんから ",end="")
                    f=1
                    c+=1
            print()
        else: #掲示板を出力する。
            print("-----------------------------")
            print("board=")
            print()
            print(data)
            print()
            print("-----------------------------")
            print()

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip="localhost"
    port = 50000
    soc.connect((ip, port))
    recp_thread = threading.Thread(target=reception_handler, args=(soc,), daemon=True)
    recp_thread.start()

    name=input('input_your_name >>')#while 1 に入る前に、名前を入力させる
    print()

    while 1:
        print(name, "さん")
        mode=input("i: send_sessage, b: check_board, d: direct_message, q: quit >> ")#モード選択をさせる
        print()
        soc.send(mode.encode())
        if mode=="i":#掲示板にメッセージの追加。その際、時間も一緒に送る。
            message = input("send_message >> ")
            print()
            send_message=message
            data=["("+datetime.now().strftime("%Y/%m/%d %H:%M:%S")+")"+name, send_message]#名前と時間を一緒の文字列する。
            data = str(data).encode()
            soc.send(data)
        elif mode=="b":#メッセージの受け取り自体はreception_handlerが行う。が、一瞬sleepした方がCUIの表示がきれい。
            sleep(0.1)
        elif mode=="d":#ダイレクトメッセージを送る。
            dmessage="###"+name+"###"+input('input_direct_message >>')
            soc.send(dmessage.encode())
        elif mode=="q":#正常終了する。
            break
        else:
            print("Error!")

if __name__ == '__main__':
    main()
