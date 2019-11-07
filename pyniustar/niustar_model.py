import mysql.connector as sql
import time
import emoji

class NiuStarModel:

    def __init__(self):
        self.dy_db = sql.connect(host='127.0.0.1', database='crawler', user='root')
        self.dy_cursor = self.dy_db.cursor(dictionary=True)
        self.record_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.user_id = ''
        self.min_aweme_id = ''

    def set_id(self, user_id, min_aweme_id):
        self.user_id = user_id
        self.min_aweme_id = min_aweme_id

    def add_user_statistics(self, data):
        one_row = (
            self.user_id,
            self.min_aweme_id,
            self.record_time,
            data['post_count'],
            data['like_count'],
            data['focus_count'],
            data['follow_count'],
            data['digg_count'],
        )
    
        sql = "INSERT INTO niustar_user_statistics (user_id, min_aweme_id, record_time, post_count, like_count, focus_count, follow_count, digg_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.dy_cursor.execute(sql, one_row)
        self.dy_db.commit()
        return True

    def add_post(self, aweme_list):
        post_arr = []
        for i in range(len(aweme_list)):
            post_row = (
                self.user_id,
                aweme_list[i]['aweme_id'],
                aweme_list[i]['aweme_type'],
                emoji.demojize(aweme_list[i]['desc']),
                aweme_list[i]['video']['vid'],
                aweme_list[i]['video']['cover']['url_list'][0],
                aweme_list[i]['video']['download_addr']['url_list'][0],
                aweme_list[i]['video']['download_addr']['url_list'][1],
                aweme_list[i]['video']['play_addr']['url_list'][0],
                aweme_list[i]['video']['play_addr']['url_list'][1],
                aweme_list[i]['video']['duration'],
                aweme_list[i]['video']['ratio'],
                aweme_list[i]['video']['width'],
                aweme_list[i]['video']['height'],
            )
            post_arr.append(post_row)

        sql = "INSERT INTO niustar_post (user_id, aweme_id, aweme_type, `desc`, vid, cover_url, download_addr_0, download_addr_1, play_addr_0, play_addr_1, duration, ratio, width, height) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE aweme_type=VALUES(aweme_type), `desc`=VALUES(`desc`), vid=VALUES(vid), cover_url=VALUES(cover_url), download_addr_0=VALUES(download_addr_0), download_addr_1=VALUES(download_addr_1), play_addr_0=VALUES(play_addr_0), play_addr_1=VALUES(play_addr_1), duration=VALUES(duration), ratio=VALUES(ratio), width=VALUES(width), height=VALUES(height)"
        self.dy_cursor.executemany(sql, post_arr)
        self.dy_db.commit()
        return True

    def add_post_statistics(self, aweme_list):
        post_statistics_arr = []
        for i in range(len(aweme_list)):
            post_statistics_row = (
                self.user_id,
                aweme_list[i]['aweme_id'],
                self.record_time,
                aweme_list[i]['statistics']['play_count'],
                aweme_list[i]['statistics']['comment_count'],
                aweme_list[i]['statistics']['digg_count'],
                aweme_list[i]['statistics']['forward_count'],
                aweme_list[i]['statistics']['share_count'],
            )
            post_statistics_arr.append(post_statistics_row)

        sql = "INSERT INTO niustar_post_statistics (user_id, aweme_id, record_time, play_count, comment_count, digg_count, forward_count, share_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.dy_cursor.executemany(sql, post_statistics_arr)
        self.dy_db.commit()
        return True

    def get_user_list(self, uid_arr = []):
        sql = "SELECT * FROM niustar_user WHERE deleted_at IS NULL"

        if uid_arr:
            sql += " AND user_id IN (%s)" % ",".join(['%s'] * len(uid_arr))

        self.dy_cursor.execute(sql, uid_arr)
        user_list = self.dy_cursor.fetchall()     # fetchall() 获取所有记录
        return user_list

    def add_user(self, user):

        sql = "INSERT INTO niustar_user (user_id, username, short_url, min_aweme_id, avatar_url, gid, douyin_account, wechat_account, realname) VALUES (%(user_id)s, %(username)s, %(short_url)s, %(min_aweme_id)s, %(avatar_url)s, %(gid)s, %(douyin_account)s, %(wechat_account)s, %(realname)s) ON DUPLICATE KEY UPDATE username=VALUES(username), short_url=VALUES(short_url), avatar_url=VALUES(avatar_url)"
        self.dy_cursor.execute(sql, user)
        self.dy_db.commit()
        return True

    # Find Least Recently aweme_id
    def find_lr_aweme_id(self, user_id, last_record_time):
        sql = "SELECT aweme_id FROM niustar_post_statistics WHERE user_id = '%s' AND record_time = '%s' ORDER BY aweme_id DESC limit 0,1" % (user_id, last_record_time)
        self.dy_cursor.execute(sql)
        post = self.dy_cursor.fetchone()
        if post:
            return post['aweme_id']
        else:
            self.add_user_retry_log()
            return 0

    def check_post(self):
        sql = "SELECT aweme_id FROM niustar_post_statistics WHERE user_id = '%s' AND record_time = '%s' ORDER BY aweme_id ASC limit 0,1" % (self.user_id, self.record_time)
        self.dy_cursor.execute(sql)
        post = self.dy_cursor.fetchone()

        if post is None and self.min_aweme_id != 0 or post['aweme_id'] > self.min_aweme_id:
            self.add_user_retry_log()

        return

    def add_user_retry_log(self):
        user = {'user_id':self.user_id, 'min_aweme_id':self.min_aweme_id, 'record_time':self.record_time}
        sql = "INSERT INTO niustar_user_retry (user_id, min_aweme_id, record_time) VALUES (%(user_id)s, %(min_aweme_id)s, %(record_time)s)"
        self.dy_cursor.execute(sql, user)
        self.dy_db.commit()
        return True
