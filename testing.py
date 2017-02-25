import pymysql

db = pymysql.connect(
    host='sql6.freesqldatabase.com',
    user='sql6159603',
    password='ISK4JfmVq9',
    charset='UTF8',
    db='sql6159603',
    cursorclass=pymysql.cursors.DictCursor)


with db.cursor() as c1:
    c1.execute('SELECT * from options where q_id = 1')
    print(c1.fetchall())

with db.cursor() as c2:
    c2.execute('select * from options where q_id = "{}" AND option_id = "{}"' \
    .format('1','1'))
    print(c2.fetchall())

with db.cursor() as c3:
    c3.execute('SELECT * FROM questions WHERE id = 8')
    print(c3.fetchall())

with db.cursor() as c4:
    c4.execute('SELECT id, name, life, coins, current_step FROM users WHERE name ="{}"'.format('shiran'))
    print(c4.fetchall())
