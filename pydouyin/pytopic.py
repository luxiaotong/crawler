from dy_model import DYModel
from dy_crawler import DYCrawler

crawler = DYCrawler()
model = DYModel()

print("Crawler Start to Run..............")
crawler.run_topic(model)


print("Crawler End to Run!")
