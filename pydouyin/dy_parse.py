from bs4 import BeautifulSoup

class DYParse:

    _num_map = {
        #0
        ' \ue603 ':'0',
        ' \ue60d ':'0',
        ' \ue616 ':'0',
        #1
        ' \ue602 ':'1',
        ' \ue60e ':'1',
        ' \ue618 ':'1',
        #2
        ' \ue605 ':'2',
        ' \ue610 ':'2',
        ' \ue617 ':'2',
        #3
        ' \ue604 ':'3',
        ' \ue611 ':'3',
        ' \ue61a ':'3',
        #4
        ' \ue606 ':'4',
        ' \ue60c ':'4',
        ' \ue619 ':'4',
        #5
        ' \ue607 ':'5',
        ' \ue60f ':'5',
        ' \ue61b ':'5',
        #6
        ' \ue608 ':'6',
        ' \ue612 ':'6',
        ' \ue61f ':'6',
        #7
        ' \ue60a ':'7',
        ' \ue613 ':'7',
        ' \ue61c ':'7',
        #8
        ' \ue60b ':'8',
        ' \ue614 ':'8',
        ' \ue61d ':'8',
        #9
        ' \ue609 ':'9',
        ' \ue615 ':'9',
        ' \ue61e ':'9',
    }

    def get_num(self, num_html):
        num_arr = []
        for i in range(len(num_html.contents)):
            num_content = num_html.contents[i]
            if num_content == ' ': continue
            if num_content != '.' and num_content != 'w ':
                num_arr.append(self._num_map[num_content.get_text()])
            else:
                num_arr.append(num_content)
        return ''.join(num_arr)

    def process_user_data(self, page_html):
        soup = BeautifulSoup(page_html, 'html.parser')
        post_num_html = soup.find('div', class_='user-tab').find('span')
        like_num_html = soup.find('div', class_='like-tab').find('span')
        focus_num_html = soup.find('span', class_='focus').find('span')
        follow_num_html = soup.find('span', class_='follower').find('span')
        digg_num_html = soup.find('span', class_='liked-num').find('span')
        post_num = self.get_num(post_num_html)
        like_num = self.get_num(like_num_html)
        focus_num = self.get_num(focus_num_html)
        follow_num = self.get_num(follow_num_html)
        digg_num = self.get_num(digg_num_html)
        #print('作品:', post_num)
        #print('喜欢:', like_num)
        #print('关注:', focus_num)
        #print('粉丝:', follow_num)
        #print('获赞:', digg_num)

        return {
            'post_count': post_num,
            'like_count': like_num,
            'focus_count': focus_num,
            'follow_count': follow_num,
            'digg_count': digg_num,
        }
