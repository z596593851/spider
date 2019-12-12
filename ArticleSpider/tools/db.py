import os
import MySQLdb
import MySQLdb.cursors
import os
from ArticleSpider.tools.analy import *

pdf_path='D:\doc\szse_pdf'
new_path='D:\doc\pdfs2'

def update_sse(docPath,quCount,wordCount):
    conn = MySQLdb.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='root',
        db='test',
        charset='utf8'
    )
    cursor = conn.cursor()
    try:
        sql = "update sse2 set wordCount ={2}, quCount={1} where docPath = '{0}'".format(docPath,quCount,wordCount)
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()

    cursor.close()
    conn.close()

def update_szse(docPath,quCount,wordCount):
    conn = MySQLdb.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='root',
        db='test',
        charset='utf8'
    )
    cursor = conn.cursor()
    try:
        sql = "update szse set wordCount ={2}, quCount={1} where docPath = '{0}'".format(docPath,quCount,wordCount)
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()

    cursor.close()
    conn.close()


def select():
    conn = MySQLdb.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='root',
        db='test',
        charset='utf8'
    )
    cursor = conn.cursor()
    try:
        sql = "select * from t_user"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            row0=row[0]
            row1 = row[1]
            print(row0,row1)
    except Exception as e:
        print(e)

    cursor.close()
    conn.close()

# if __name__ == '__main__':
#     path="D:\\doc\\sse\\"
#     files=os.listdir(path)
#     i=1
#     for file in files:
#         page_count, word_count=analy_doc(path+file)
#         print(file)
#         update_sse(file.split(".")[0]+".pdf",page_count, word_count)
#         print(i)
#         i+=1;

if __name__ == '__main__':
    path="D:\\doc\\szse_pdf\\"
    files=os.listdir(path)
    i=1
    for file in files:
        print(file)
        try:
            page_count, word_count=analy_doc(path+file)
            update_szse(file, page_count, word_count)
            # print(page_count, word_count)
        except Exception as e:
            print(e)
            continue
        # update_sse(file.split(".")[0]+".pdf",page_count, word_count)
        print(i)
        i+=1









