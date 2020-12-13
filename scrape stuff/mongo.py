

import pymongo



client = pymongo.MongoClient("mongodb+srv://daniel:bebatheBear21@datacluster.htvsb.mongodb.net/wine_and_cheese?retryWrites=true&w=majority")


db = client.wine_and_cheese

cols = db.list_collection_names()

for i in cols:
	print(i)







