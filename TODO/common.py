# coding=utf-8
from TODO.models import list
import time
from datetime import date, datetime, timedelta
import traceback
from django.contrib.auth.models import User
import pymysql.cursors


class DBAction():
    def __init__(self):
        pass

    def create(self, **pam):
        add_time = str(time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        list.objects.create(content=pam['content'], level=pam['level'], add_time=add_time,
                            is_complete=pam['is_complete'], user_id=pam[
                'user_id'], is_send_mail=0,
                            time_day=pam['time_day'], time_hours=pam['time_hours'], time_minute=pam['time_minute'])

    def query(self, user_id):
        user = User.objects.get(id=int(user_id))
        return user.user_list.all()

    def update(self, id):
        try:
            complete_time = str(time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            list.objects.filter(id=int(id)).update(
                complete_time=complete_time, is_complete="1")
        except:
            traceback.print_exc()

    def del_list(self, id):
        list.objects.filter(id=int(id)).delete()

    def updata_content(self, id, content):
        try:
            list.objects.filter(id=int(id)).update(content=content)
        except:
            traceback.print_exc()

    def query_all(self):
        return list.objects.all()

    def search_all(self, user_id, q_set):
        return list.objects.filter(q_set).filter(user_id=user_id).all()


class DBActionMYSQL():
    '''
    MYSQL 操作
    '''
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '123123',
        'db': 'news',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }

    def __init__(self):
        self.conn = pymysql.connect(**self.config)

    def query(self):
        result = []
        try:
            with self.conn.cursor() as cursor:
                sql = 'SELECT * FROM ifeng_news order by news_time desc'
                cursor.execute(sql)
                result = cursor.fetchall()
                self.conn.commit()
        finally:
            self.conn.close()
            return result
    def delete(self):
        r = False
        try:
            with self.conn.cursor() as cursor:
                sql = 'TRUNCATE ifeng_news'
                r = cursor.execute(sql)
                self.conn.commit()
        except Exception,e:
            print e
        finally:
            self.conn.close()
            return r