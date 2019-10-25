import mysql.connector as sql
import time
import emoji

class DYModel:

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
            self.record_time,
            data['post_count'],
            data['like_count'],
            data['focus_count'],
            data['follow_count'],
            data['digg_count'],
        )
    
        sql = "INSERT INTO douyin_user_statistics (user_id, record_time, post_count, like_count, focus_count, follow_count, digg_count) VALUES (%s, %s, %s, %s, %s, %s, %s)"
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

        sql = "INSERT INTO douyin_post (user_id, aweme_id, aweme_type, `desc`, vid, cover_url, download_addr_0, download_addr_1, play_addr_0, play_addr_1, duration, ratio, width, height) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE aweme_type=VALUES(aweme_type), `desc`=VALUES(`desc`), vid=VALUES(vid), cover_url=VALUES(cover_url), download_addr_0=VALUES(download_addr_0), download_addr_1=VALUES(download_addr_1), play_addr_0=VALUES(play_addr_0), play_addr_1=VALUES(play_addr_1), duration=VALUES(duration), ratio=VALUES(ratio), width=VALUES(width), height=VALUES(height)"
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

        sql = "INSERT INTO douyin_post_statistics (user_id, aweme_id, record_time, play_count, comment_count, digg_count, forward_count, share_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.dy_cursor.executemany(sql, post_statistics_arr)
        self.dy_db.commit()
        return True

    def get_user_list(self):
        self.dy_cursor.execute("SELECT * FROM douyin_user where deleted_at IS NULL")
        user_list = self.dy_cursor.fetchall()     # fetchall() 获取所有记录
        return user_list

    def add_user(self, user):

        sql = "INSERT INTO douyin_user (user_id, username, short_url, avatar_url) VALUES (%(user_id)s, %(username)s, %(short_url)s, %(avatar_url)s) ON DUPLICATE KEY UPDATE username=VALUES(username), short_url=VALUES(short_url), avatar_url=VALUES(avatar_url)"
        self.dy_cursor.execute(sql, user)
        self.dy_db.commit()
        return True

    def add_topic_post(self, post_list):
        sql = "INSERT INTO douyin_topic_post (topic_name, aweme_id) VALUES (%(topic_name)s, %(aweme_id)s) ON DUPLICATE KEY UPDATE topic_name=VALUES(topic_name), aweme_id=VALUES(aweme_id)"
        self.dy_cursor.executemany(sql, post_list)
        self.dy_db.commit()
        return True
