import socket, threading
from multiprocessing import Value, Array

def recp_handler(soc, ip, port, point, board):
    while 1:
        mode=soc.recv(1024).decode()
        print(mode)
        if mode=="i":
            message = soc.recv(1024).decode()
            print('Recv_message >> {}'.format(message))
            my_name=""
            send_message=""
            f=1
            print(message)
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
            print("name=",my_name)
            print("mess=",send_message)
            tempp=+point.value
            for i,j in enumerate(my_name):
                board[i+tempp]=j.encode()
                point.value+=1
            board[point.value]="\n".encode()
            point.value+=1
            tempp=+point.value
            for i,j in enumerate(send_message):
                print(i,j)
                board[i+tempp]=j.encode()
                point.value+=1
            board[point.value]="\n".encode()
            point.value+=1
        elif mode=="b":
            sendb=""
            for i in range(point.value):
                sendb+=board[i].decode()
            soc.send(sendb.encode())
        elif mode=="q":
            soc.close()
            print('Bye-Bye: {0}:{1}'.format(ip, port))
            break


def main():
    count = Value('i', 0)
    name_array = Array('c', 1024)

    ssoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    ip="localhost"
    port = 50007
    ssoc.bind((ip, port))    # 指定したホスト(IP)とポートをソケットに設定
    ssoc.listen(5)                     # 1つの接続要求を待つ

    while 1:
        csoc, addr = ssoc.accept() 
        print("Conneted by"+str(addr))
        # 接続してきたクライアントを処理するスレッドを用意する
        client_thread = threading.Thread(target=recp_handler, args=(csoc,ip,port,count,name_array))
        # 親 (メイン) スレッドが死んだら子も道連れにする
        client_thread.daemon = True
        # スレッドを起動する
        client_thread.start()

if __name__ == '__main__':
    main()
