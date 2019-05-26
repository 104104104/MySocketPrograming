import socket, threading
from multiprocessing import Value, Array

def recp_handler(soc, ip, port, point, board, addr):
    while 1:
        mode=soc.recv(1024).decode() #modeを受け取る。これに応じてserverは動きを変える。
        print(mode)
        if mode=="i": #掲示板(board)に文字列を追加する。
            print("mode_input")
            message = soc.recv(1024).decode()
            my_name=""
            send_message=""
            f=1
            p=0
            while p < len(message):
                if message[p] not in ["[", "]", "'"]:#list型を受け取るので、解析する。適宜名前とメッセージに分解
                    if message[p]==",":
                        f=0
                        p+=3
                    if f:
                        my_name+=message[p]
                    else:
                        send_message+=message[p]
                p+=1
            my_name=my_name.strip()
            send_message=send_message.strip()
            tempp=+point.value
            for i,j in enumerate(my_name):#掲示板(board)にまずは名前を追加。multiprocessingのArrayを使ってみので、multiprocessingのvalue型のint型の変数をポインタとして使う必要があった。
                board[i+tempp]=j.encode()
                point.value+=1
            board[point.value]="\n".encode()
            point.value+=1
            tempp=+point.value
            for i,j in enumerate(send_message):#こちらでは、メッセージ本体を追加。
                board[i+tempp]=j.encode()
                point.value+=1
            board[point.value]="\n".encode()
            point.value+=1
        elif mode=="b":#boardをclientに送信しているだけ。
            print("mode_board")
            sendb=""
            for i in range(point.value):
                sendb+=board[i].decode()
            soc.send(sendb.encode())
        elif mode=="d":#ダイレクトメッセージモード。
            print("mode_direct")
            dmessage=soc.recv(1024)
            print(dmessage)
            for c in clients:#全員に送る。
                 c[0].sendto(dmessage, c[1])
        elif mode=="q":#終了する。clientsから自分のsocketを消しておく必要がある。
            clients.remove((soc, addr))
            soc.close()
            print('Bye-Bye: {0}:{1}'.format(ip, port))
            break


def main():
    global clients
    print("server_on")
    clients=[]
    count = Value('i', 0)
    name_array = Array('c', 1024)

    ssoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    ip="localhost"
    port = 50000
    ssoc.bind((ip, port))
    ssoc.listen(1)

    while 1:
        csoc, addr = ssoc.accept()          # 要求が来るまでブロック
        clients.append((csoc, addr))
        print("Conneted by"+str(addr))
        # 接続してきたクライアントを処理するスレッドを用意する
        client_thread = threading.Thread(target=recp_handler, args=(csoc,ip,port,count,name_array, addr))
        client_thread.daemon = True
        client_thread.start()

if __name__ == '__main__':
    main()
