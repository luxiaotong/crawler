from niustar_model import NiuStarModel
from niustar_crawler import NiuStarCrawler
from utils import get_params


crawler = NiuStarCrawler()
model = NiuStarModel()

uids, last_record_time = get_params()
if uids:
    uid_arr = uids.split(",")
    user_list = model.get_user_list(uid_arr)
else:
    user_list = model.get_user_list()


for user in user_list:
    print("Crawler Start to Run..............")
    print("username:", user['username'])
    print("userid:", user['user_id'])
    print("short_url:", user['short_url'])
    min_aweme_id = model.find_lr_aweme_id(user['user_id'], last_record_time)
    #min_aweme_id = user['min_aweme_id']
    print("min_aweme_id:", min_aweme_id)
    model.set_id(user['user_id'], min_aweme_id)
    crawler.run(model)

    print("-"*20 + user['username'] + " Finished" + "-"*20)
    print()


print("Crawler End to Run!")
