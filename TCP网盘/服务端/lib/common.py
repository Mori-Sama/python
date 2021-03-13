import json
import struct
import hashlib
import os


def msg_unpack_recv(conn):
    try:
        head = conn.recv(4)
        msg_len = struct.unpack('i', head)[0]
        msg = conn.recv(msg_len)
    except Exception:
        conn.close()
        return {'sync':0}
    return json.loads(msg.decode('utf-8'))


def ency(password):
    m = hashlib.md5('赵徐璐'.encode('utf-8'))
    m.update(password.encode('utf-8'))
    password = m.hexdigest()
    return password


def show_dir_list(path):
    x = next(os.walk(path))
    current_dir = x[0]
    file_list = x[1] + x[2]
    return current_dir,file_list


def msg_pack_send(user_dict,conn):
    user_dict = json.dumps(user_dict).encode('utf-8')
    head = struct.pack('i',len(user_dict))
    conn.send(head)
    conn.send(user_dict)

