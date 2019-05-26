import socket, threading
from multiprocessing import Value, Array

def recp_handler(soc, ip, port, count, name_array):
    myname=soc.recv(1024).decode()
    print(myname)
    if len(myname)>5:
            print('Error!: {0}:{1}'.format(ip, port))
            soc.close()
    for i in range(len(myname)):
        #print(i, count.value, myname[i],type(i),type(count.value),type(myname[i], type(name_array[i+count.value])))
        name_array[i+count.value]=myname[i].encode()
    count.value+=5

    while 1:
        message = soc.recv(1024).decode()
        print("cliant_name_is", myname)
        print('Recv_message >> {}'.format(message))
        from_name=myname
        to_name=""
        send_message=""
        f=1
        for i in message:
            print(i)
            if i not in ["[", "]", ","]:#list型を受け取るので、解析する。適宜宛先とメッセージに分解
                if i==",":
                    f=0
                if f:
                    to_name+=i
                else:
                    send_message+=i
        print(to_name, send_message)

        # 受信したデータをそのまま送り返す (エコー)
#        if not message:
#            break
        soc.send(send_message.encode())
        print("{0}:{1}にオウム返しシマシタ".format(ip, port))
    soc.close()
    print('Bye-Bye: {0}:{1}'.format(ip, port))


def main():
    count = Value('i', 0)
    name_array = Array('c', 15) #nameは5文字まで。三人まで使える。

    ssoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    ip="localhost"
    port = 50007
    ssoc.bind((ip, port))    # 指定したホスト(IP)とポートをソケットに設定
    ssoc.listen(5)                     # 1つの接続要求を待つ

    while 1:
        csoc, addr = ssoc.accept()          # 要求が来るまでブロック
        print("Conneted by"+str(addr))  #サーバ側の合図
        # 接続してきたクライアントを処理するスレッドを用意する
        client_thread = threading.Thread(target=recp_handler, args=(csoc,ip,port,count,name_array))
        # 親 (メイン) スレッドが死んだら子も道連れにする
        client_thread.daemon = True
        # スレッドを起動する
        client_thread.start()

if __name__ == '__main__':
    main()
