#!myvenv/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
import pymongo

'''

Fire Emblem Heroes API V1.0

@author john-f2


notes
-----
• consider chaning name into two fields, name and epithet

'''

app = Flask(__name__)

#default route
@app.route('/')
def index():
	return 'Fire Emblem Heroes API V1.0'

########################################################
''' mongodb setup (Don't forget to start the server) '''
########################################################

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client['feh_api']

#collections 
heroes_col = db['heroes']
weapons_col = db['weapons']
skills_col = db['skills']
assists_col = db['assists']
special_col = db['specials']




#####################
''' GET Functions '''
#####################

@app.route('/feh/api/v1.0/heroes', methods=['GET'])
def get_all_heroes():
	''' returns json object of all heroes in the heroes collection '''
	return jsonify({ 'Heroes' : list(heroes_col.find())})

@app.route('/feh/api/v1.0/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
	''' Returns a hero with matching id '''

	find_hero = list(heroes_col.find({"_id":hero_id}))

	if len(find_hero) == 0:
		#if id not found return 404 error
		abort(404)
	return jsonify({'heroes':find_hero}) 



#######################
''' POST FUNCTIONS  '''
#######################


@app.route('/feh/api/v1.0/heroes', methods=['POST'])
def add_hero():
	''' Adds a new hero to the heroes collection '''

	#if the reqest is not in json format or does not have a 'name' value
	#then abort 
	if not request.json or not 'name' in request.json:
		abort(404)

	#gets the latest hero id from the collection
	next_id = list(heroes_col.find({}, {'_id':1}).limit(1).sort('$natural',-1))


	new_hero = {
		'_id' : next_id[0]['_id']+1,
		'name': request.json['name'],
		'description': request.json.get('description', ""), 
		'rarities': request.json.get('rarities', ""),
		'w_type': request.json.get('w_type', ""),
		'm_type': request.json.get('m_type', ""),
		'origin' : request.json.get('origin', ""),
		'weapons': request.json.get('weapons', ""),
		'assists': request.json.get('assists', ""),
		'specials': request.json.get('specials', ""),
		'passives': request.json.get('passives', "") ,
		'stats': request.json.get('stats', "") ,
		'growth_points': request.json.get('growth_points', "")

	}

	#adds the new hero to the collection
	heroes_col.insert_one(new_hero)

	#returns back the json of the new hero and a 201 status code meaning "created"
	return jsonify({'Added Hero': new_hero}), 201









if __name__ == '__main__':
	#starts flask server
	app.run(debug=True)