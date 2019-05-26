import socket, threading
from multiprocessing import Value, Array

def recp_handler(soc, ip, port, point, board,clientnum,client_array, client_array_point):
    name=soc.recv(1024).decode()
    if len(name)!=4:
        print("Error_name_length")
    client_num.value+=1
    client_array[client_array_point.value]=str(client_num.value)
    client_num.value+=1
    for i in name:
        client_array[client_array_point.value]=i
        client_array_point.value+=1
    print(client_array)

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
        elif mode=="d":
            message = soc.recv(1024).decode()
            print(message)
            from_name=""
            to_name=""
            send_message=""
            f1=1
            f2=1
            print(message)
            p=0
            while p < len(message):
                if message[p] not in ["[", "]", "'"]:#list型を受け取るので、解析する。適宜名前とメッセージに分解
                    if message[p]==",":
                        f1=0
                        p+=3
                    if f1 and message[p]==",":
                        f1=0
                        p+=3
                    if f1:
                        from_name+=message[p]
                    elif f1 and f2:
                        to_name+=message[p]
                    else:
                        send_message+=message[p]
                p+=1
            from_name=from_name.strip()
            to_name=to_name.strip()
            send_message=send_message.strip()

            #for i in range(client_array_point.value):


        elif mode=="q":
            soc.close()
            print('Bye-Bye: {0}:{1}'.format(ip, port))
            break


def main():
    count = Value('i', 0)
    board = Array('c', 1024)
    client_num = Value('i', 1)
    client_array = Array('c', 1024)
    client_array_point=Value('i', 0)

    ssoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    ip="localhost"
    port = 50000
    ssoc.bind((ip, port))
    ssoc.listen(1)
    csoc.send(str(client_num.value).encode())

    #dsocはdirectmessage用
    dsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dsoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    dip="localhost"
    dport = 50000+client_num.value
    dsoc.bind((dip, dport))
    client_num.value+=1
    dsoc.listen(1)

    while 1:
        csoc, addr = ssoc.accept()
        print("Conneted by"+str(addr))
        # 接続してきたクライアントを処理するスレッドを用意する
        client_thread = threading.Thread(target=recp_handler, args=(csoc,ip,port,count,board,client_num,client_array, client_array_point))
        # 親 (メイン) スレッドが死んだら子も道連れにする
        client_thread.daemon = True
        # スレッドを起動する
        client_thread.start()

if __name__ == '__main__':
    main()
