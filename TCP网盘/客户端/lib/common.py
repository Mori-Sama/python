import json
import struct


def msg_pack_send(user_dict,sock):
    user_dict = json.dumps(user_dict).encode('utf-8')
    head = struct.pack('i',len(user_dict))
    sock.send(head)
    sock.send(user_dict)


def msg_unpack_recv(sock):
    head = sock.recv(4)
    msg_len = struct.unpack('i',head)[0]
    msg = sock.recv(msg_len)
    return json.loads(msg.decode('utf-8'))


def send_sync(sock,number):
    sync_dict = {'sync':number}
    msg_pack_send(sync_dict,sock)


def show_file_list(file_list):
    file_list = enumerate(file_list,0)
    for i in file_list:
        print(i)

