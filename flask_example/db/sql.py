import pymysql
from flask_example.setting.setting import HOSTNAME, USERNAME, PASSWORD, DATABASE


def sql_1():
    con = None
    try:
        con = pymysql.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE)
        cur = con.cursor()
        cur.execute("select version()")
        ver = cur.fetchone()
        print("Database version: {}".format(ver[0]))
    except Exception as e:
        print("Error {}:{}".format(e.args[0], e.args[1]))
        exit(1)
    finally:
        if con:
            con.close()


def sql_2():
    con = pymysql.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE)
    with con as cur:
        cur.execute("select version()")
        rows = cur.fetchall()
        for row in rows:
            print(row[0])


if __name__ == "__main__":
    # main()
    db()
