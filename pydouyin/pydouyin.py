from dy_model import DYModel
from dy_crawler import DYCrawler

crawler = DYCrawler()
model = DYModel()
user_list = model.get_user_list()

for user in user_list:
    print("Crawler Start to Run..............")
    print("username:", user['username'])
    print("userid:", user['user_id'])
    print("min_aweme_id:", user['min_aweme_id'])
    print("short_url:", user['short_url'])
    model.set_id(user['user_id'], user['min_aweme_id'])
    crawler.run(model)

    print("User " + user['username'] + " Finished........")


print("Crawler End to Run!")
