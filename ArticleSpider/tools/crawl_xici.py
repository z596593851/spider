from scrapy.selector import Selector
import requests
import re
import MySQLdb

conn=MySQLdb.connect(host="127.0.0.1",user="root",passwd="root",db="doubandb",charset="utf8")
cursor=conn.cursor( )
ip_rule=".*[>](.*)[<].*"
def xici_ip():
    header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}
    for i in range(5):

        response = requests.get("https://www.xicidaili.com/nn/{}".format(i), headers=header)
        selector=Selector(text=response.text)
        all_trs=selector.css("#ip_list tr")
        ip_list=[]
        #print(all_trs.extract())
        for tr in all_trs[1:]:
            tds=tr.css("td")
            #all_texts=tr.css("td::text").extract()
            ip_o=tds[1].extract()
            ip_r=re.match(ip_rule,ip_o).group(1)
            port_o=tds[2].extract()
            port_r=re.match(ip_rule,port_o).group(1)
            proxy_type_o=tds[5].extract()
            proxy_type_r=re.match(ip_rule,proxy_type_o).group(1)
            ip_list.append((ip_r,port_r,proxy_type_r))
        for ip_info in ip_list:
            cursor.execute(
                "insert proxy_ip_2(ip,port,proxy_type) VALUES('{0}','{1}','{2}')".format(
                    ip_info[0],ip_info[1],ip_info[2]
                )
            )
            conn.commit()

class GetIP(object):
    def delete_ip(self,ip):
        delete_sql="""
            delete from proxy_ip where ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self,ip,port,proxy_type):
        #判断IP是否可用
        h="http"
        if proxy_type=="HTTP":
            h="http"
        elif proxy_type=="HTTPS":
            h="https"
        http_url="https://www.baidu.com"
        proxy_url="{0}://{1}:{2}".format(h,ip,port)
        try:
            proxy_dict = {
                h: proxy_url
            }
            response=requests.get(http_url,proxies=proxy_dict)

        except Exception as e:
            print("invalid ip and port:{0}:{1}".format(ip,port))
            self.delete_ip(ip)
            return False
        else:
            code=response.status_code
            if code>=200 and code<300:
                print("effective ip:{0}:{1}".format(ip,port))
                return True
            else:
                print("invalid ip and port:{0}:{1}".format(ip, port))
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        random_sql="""
            SELECT ip,port,proxy_type FROM proxy_ip_2
            ORDER BY RAND()
            LIMIT 1
        """
        result=cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip=ip_info[0]
            port=ip_info[1]
            proxy_type=ip_info[2]
            judge_re=self.judge_ip(ip,port,proxy_type)
            if judge_re:
                h=''
                if proxy_type=='HTTP':
                    h='http'
                elif proxy_type=='HTTPS':
                    h='https'
                print("{0}://{1}:{2}".format(h,ip,port))
                return "{0}://{1}:{2}".format(h,ip,port)
            else:
                return self.get_random_ip()


if __name__ == '__main__':
    xici_ip()
    # get_ip=GetIP()
    # get_ip.get_random_ip()


