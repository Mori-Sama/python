import pymysql

conn = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = '1181801087',
    database = 'zhaoxulu',
    charset = 'utf8'
)
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)


def select(username):
    sql = 'select username,password from user where username=%s'
    cursor.execute(sql, (username,))
    user_dict = cursor.fetchone()
    return user_dict


def create(username,password):
    sql = 'insert into user(username,password) value(%s,%s)'
    cursor.execute(sql,(username,password))
    conn.commit()