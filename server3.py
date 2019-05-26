# -*- coding: utf-8 -*-
import socket, threading

def client_handler(soc, ip, port):
    while 1:
        message = soc.recv(1024)
        print('Recv_message >> {}'.format(message))
        # 受信したデータをそのまま送り返す (エコー)
        if not message:
            break
        sent_message = message
        soc.send(sent_message)
        print("{0}:{1}にオウム返しシマシタ".format(ip, port))
    soc.close()
    print('Bye-Bye: {0}:{1}'.format(ip, port))


def main():
    ssoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    ip="localhost"
    port = 50007
    ssoc.bind((ip, port))    # 指定したホスト(IP)とポートをソケットに設定
    ssoc.listen(1)                     # 1つの接続要求を待つ

    while 1:
        csoc, addr = ssoc.accept()          # 要求が来るまでブロック
        print("Conneted by"+str(addr))  #サーバ側の合図
        # 接続してきたクライアントを処理するスレッドを用意する
        client_thread = threading.Thread(target=client_handler, args=(csoc,ip,port))
        # 親 (メイン) スレッドが死んだら子も道連れにする
        client_thread.daemon = True
        # スレッドを起動する
        client_thread.start()

if __name__ == '__main__':
    main()
