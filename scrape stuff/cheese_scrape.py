import requests
import string
from bs4 import BeautifulSoup as bs
import pymongo


def get_cheese_links(letter,page):

	url = "https://www.cheese.com/alphabetical/?per_page=100&i={}&page={}#top".format(letter,page)

	page_response = requests.get(url)
	page = page_response.content
	soup = bs(page,'html.parser')

	cheese_base = "https://www.cheese.com"
	cheese_links = []

	cheeses = soup.find_all(attrs={"class":"col-sm-6 col-md-4 cheese-item text-center"})

	for i in cheeses:
		link = i.find('a')
		cheese_links.append(cheese_base+link['href'])
	
	return cheese_links

def get_cheese_info(url):

	page_response = requests.get(url)
	page = page_response.content
	soup = bs(page,'html.parser')

	cheese_info = {}

	name_obj = soup.find_all('h1')
	name = name_obj[1].contents[0]

	image_obj = soup.find_all(attrs={"class":"cheese-image"})
	image = image_obj[0].find('img')['src']
	if (image[0] != "."):
		image = ("https://www.cheese.com" + image)
	else:
		image = ""

	location_obj = soup.find(attrs={"class":"fa fa-flag"})
	if (location_obj is not None):
		location = location_obj.parent.a.contents[0]
	else:
		location = ""

	flavor_obj = soup.find(attrs={"class":"fa fa-spoon"})
	if (flavor_obj is not None):
		flavor = flavor_obj.parent.p.contents
		flavor = flavor[0][9:].split(", ")
	else:
		flavor = []

	rind_obj = soup.find(attrs={"class":"fa fa-paint-brush"})
	if (rind_obj is not None):
		rind = rind_obj.parent.p.contents[0][6:]
	else:
		rind = ""
	
	vege_obj = soup.find(attrs={"class":"fa fa-leaf"})
	if (vege_obj is not None):
		vege_text = vege_obj.parent.p.contents[0][12:]
		if (vege_text.lower() == "yes "):
			vege = True
		else:
			vege = False
	else:
		vege = None

	texture_obj = soup.find(attrs={"class":"fa fa-pie-chart"})
	if (texture_obj is not None):
		texture = texture_obj.parent.p.a.contents[0]
	else:
		texture = ""

	type_obj = soup.find(attrs={"class":"fa fa-folder-o"})
	if (type_obj is not None):
		ctype = []
		ctype_arr = type_obj.parent.p.contents
		if (len(ctype_arr) == 1):
			ctype = ctype_arr[0][6:]
		if (len(ctype_arr) > 1):
			ctype.append(ctype_arr[1].contents[0])
		if (len(ctype_arr) > 2):
			ctype.extend(ctype_arr[2][2:].split(", "))
	else:
		ctype = []

	color_obj = soup.find(attrs={"class":"fa fa-tint"})
	if (color_obj is not None):
		color = color_obj.parent.p.contents[0][8:]
	else:
		color = ""

	cheese_info["name"] = name
	cheese_info["image"] = image
	cheese_info["location"] = location
	cheese_info["flavor"] = flavor
	cheese_info["rind"] = rind
	cheese_info["vegetarian"] = vege
	cheese_info["texture"] = texture
	cheese_info["type"] = ctype
	cheese_info["color"] = color


	return cheese_info

def insert_to_mongo():
	username = input("username: ")
	password = input("passord: ")
	uri = "mongodb+srv://{}:{}@datacluster.htvsb.mongodb.net/wine_and_cheese?retryWrites=true&w=majority".format(username,password)
	client = pymongo.MongoClient(uri)

	db = client.wine_and_cheese.cheese
	# db.create_index("name",unique=True)

	letters = list(string.ascii_lowercase)

	letter = "s"

	all_links = []
	all_cheeses = []

	for i in range(2,4):
		print("gathering links",letter,"page",i)
		all_links.extend(get_cheese_links(letter,i))

	for j in range(len(all_links)):
		print("working on cheese",j,"of",len(all_links))
		all_cheeses.append(get_cheese_info(all_links[j]))
		# db.insert_many(all_cheeses,ordered=False)

	for l in all_cheeses:
		try:
			db.insert(all_cheeses)
			# print('Inserted', str(len(all_cheeses)), 'cheeses')
		except:
			print('err')
	


insert_to_mongo()



