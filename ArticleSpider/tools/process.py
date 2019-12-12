import os
import MySQLdb
import MySQLdb.cursors
import shutil
import os
from ArticleSpider.tools.analy import *

from_path='D:\\doc\\sse\\'
to_path='D:\\doc\\sse_qu\\'

def select():
    results=[]
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
        sql = "select * from sse2 where quCount=0"
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as e:
        print(e)

    cursor.close()
    conn.close()
    return results


if __name__ == '__main__':
    results=select()
    for result in results:
        print(result[5])
        shutil.copy(from_path+result[5].split(".")[0]+".docx",to_path+result[5].split(".")[0]+".docx")

