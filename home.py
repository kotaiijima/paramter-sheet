from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras
from decimal import *

app = Flask(__name__)

@app.route('/', methods=["POST","GET"])
def home():

        # データベースに接続
    connection = psycopg2.connect(host='localhost',
                              user='postgres',
                              password='Taka1579',
                              database='sampledb')
    if request.method == 'POST':
        command = request.form['command']
        match command:
            case '追加':
                tensu_1 = request.form['tensu_1']
                tensu_2 = request.form['tensu_2']
                tensu_3 = request.form['tensu_3']
                tensu_4 = request.form['tensu_4']
                insert(connection, tensu_1, tensu_2, tensu_3, tensu_4)
            case '更新':
                id = request.form['id']
                tensu_1 = request.form['tensu_1']
                tensu_2 = request.form['tensu_2']
                tensu_3 = request.form['tensu_3']
                tensu_4 = request.form['tensu_4']
                update(connection, id, tensu_1, tensu_2, tensu_3, tensu_4)
            case '削除':
                id = request.form['id']
                delete(connection, id)
        
    tensu_list, shokin = set_result(connection)
 
    return render_template(
        'home.html',
        title='年末麻雀大会',
        tensu_list = tensu_list,
        shokin = shokin
        )

def insert(connection, tensu_1, tensu_2, tensu_3, tensu_4):
        with connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        # レコードを追加
                sql = "INSERT INTO majan (tensu_1, tensu_2, tensu_3 ,tensu_4) VALUES(%s, %s, %s, %s)"
                print(sql)
                cursor.execute(sql, (tensu_1, tensu_2, tensu_3, tensu_4))
                connection.commit()

def update(connection, id, tensu_1, tensu_2, tensu_3, tensu_4):
        with connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        # レコードを追加
                sql = "UPDATE majan set tensu_1= %s, tensu_2= %s, tensu_3= %s, tensu_4= %s WHERE id = %s"
                print(sql)
                cursor.execute(sql, (tensu_1, tensu_2, tensu_3, tensu_4, id))
                connection.commit()

def delete(connection, id):
            with connection:
                with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            # レコードを追加
                    sql = "DELETE majan WHERE id = %s"
                    print(sql)
                    cursor.execute(sql, (id))
                    connection.commit()

@app.route('/insert', methods=["POST"])
def insert_bk(): 
    # データベースに接続
    connection = psycopg2.connect(host='localhost',
                              user='postgres',
                              password='Taka1579',
                              database='sampledb')
    
    tensu_1 = request.form['tensu_1']
    tensu_2 = request.form['tensu_2']
    tensu_3 = request.form['tensu_3']
    tensu_4 = request.form['tensu_4']
    print(tensu_1)

    with connection:
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        # レコードを追加
            sql = "INSERT INTO majan (tensu_1, tensu_2, tensu_3 ,tensu_4) VALUES(%s, %s, %s, %s)"
            print(sql)
            cursor.execute(sql, (tensu_1, tensu_2, tensu_3, tensu_4))
            connection.commit()

    tensu_list, shokin = set_result(connection)

    return render_template(
        'home.html',
        title='年末麻雀大会',
        tensu_list = tensu_list,
        shokin = shokin
        )

@app.route('/update', methods=["POST"])
def update(): 
    # データベースに接続
    connection = psycopg2.connect(host='localhost',
                              user='postgres',
                              password='Taka1579',
                              database='sampledb')
    
    tensu_1 = request.form['tensu_1']
    tensu_2 = request.form['tensu_2']
    tensu_3 = request.form['tensu_3']
    tensu_4 = request.form['tensu_4']
    id = request.form['id']


    with connection:
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        # レコードを更新
            sql = "UPDATE majan set tensu_1= %s, tensu_2= %s, tensu_3= %s, tensu_4= %s WHERE id = %s"
            print(sql)
            cursor.execute(sql, (tensu_1, tensu_2, tensu_3, tensu_4, id))
            connection.commit()

    tensu_list, shokin = set_result(connection)

    return render_template(
        'home.html',
        title='年末麻雀大会',
        tensu_list = tensu_list,
        shokin = shokin
        )

@app.route('/tuika')
def tuika(): 

    return render_template(
        'tuika.html',
        title='年末麻雀大会',
        )


def set_result(connection):

    with connection:
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        # レコードを取得
            sql = "SELECT * FROM majan"
            cursor.execute(sql)
            tensu_list = cursor.fetchall()
        # レコードを取得
            sql = "SELECT COUNT(*) FROM majan"
            cursor.execute(sql)
            count = cursor.fetchone()
            sum_tensu = [0, 0, 0, 0]
    for i in range(0, count[0]):
        list = tensu_list[i][:4]
        sort_list = sorted(list, reverse=True)
        for j in range(0, 4):
            idx = sort_list.index(list[j])
            match idx:
                case 0:
                    list[j] += 40000
                    sum_tensu[j] += list[j]
                case 1:
                    list[j] += 10000
                    sum_tensu[j] += list[j]
                case 2:
                    list[j] -= 10000
                    sum_tensu[j] += list[j]
                case 3:
                    list[j] -= 20000
                    sum_tensu[j] += list[j]
    shokin = [0, 0, 0, 0]
    if count[0] != 0:
        for i in range(4):
            w_shokin = ((sum_tensu[i] / count[0] - 30000) / 10 + 5000) / 1000
            shokin[i] = int(Decimal(str(w_shokin)).quantize(Decimal('0.1'), rounding=ROUND_HALF_DOWN) * 1000)
        print(shokin)    
    return tensu_list, shokin
        
if __name__ == '__main__':
    app.run(debug=True)

    