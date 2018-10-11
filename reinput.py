import pymysql
from selenium.common.exceptions import NoSuchElementException
import time
db = pymysql.connect(host='206.189.90.203',user='zun95',passwd='Hotdilvin95',db='merucali')
cursor = db.cursor()
def inserts(hre,tit,lik,sto,pri,tim):
    try:
        cursor.execute("INSERT into changes (href,title,likes,stock,price,time_update) VALUES(%s, %s, %s, %s, %s, %s)",(hre,tit,lik,sto,pri,tim))
        db.commit()
    except:
        print("error")
        db.rollback()
def get(x,h):
    try:
        cursor.execute("SELECT * FROM post WHERE href LIKE %s ORDER BY time_update ASC",(x))
        datas = cursor.fetchall()
        if len(datas) > 1:
            #main reinput
            for data in datas:

                link = data[1]
                title = data[2]
                likes = data[3]
                stock = data[4]
                prices = data[5]
                time = data[6]
                #print(link,title,likes,stock,prices,time)
                cursor.execute("SELECT * FROM changes WHERE href LIKE %s AND title LIKE %s AND likes LIKE %s AND stock LIKE %s AND price LIKE %s",(link,title,likes,stock,prices))
                datos = cursor.fetchall()
                if len(datos) >= 1:
                    print("data alaready haved")
                    break
                else:
                    inserts(link,title,likes,stock,prices,time)
                    print("insert new data to table")
        else:

            #donothings
            print(str(h),"none duplicate")
    except:
        print ("Errorget: unable to fetch data")
def main():
    try:
        cursor.execute("SELECT * FROM post ")
        datas = cursor.fetchall()
        h = 0
        for data in datas:
            link = data[1]
            h += 1
            get(link,h)
        main()
    except:
        print ("Errormain: unable to fetch data")

main()
db.close()
