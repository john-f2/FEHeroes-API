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
accessories_col = db['accessories']





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


@app.route('/feh/api/v1.0/weapons', methods=['GET'])
def get_all_weapons():
	''' Returns a json of all weapons '''
	return jsonify({'weapons': list(weapons_col.find())})

@app.route('/feh/api/v1.0/weapons/<int:weapon_id>', methods=['GET'])
def get_weapon(weapon_id):
	'''Returns a weapon with matching id '''
	find_weapon = list(weapons_col.find({"_id":weapon_id}))
	if len(find_weapon) == 0:
		abort(404)
	return jsonify({'weapons':find_weapon})


@app.route('/feh/api/v1.0/skills', methods=['GET'])
def get_all_skills():
	''' Returns a json of all skills '''
	return jsonify({'skills':list(skills_col.find())})

@app.route('/feh/api/v1.0/skills/<int:skill_id>', methods=['GET'])
def get_skill(skill_id):
	'''Returns a weapon with matching id '''
	find_skill = list(skills_col.find({"_id":skill_id}))
	if len(find_skill) == 0:
		abort(404)
	return jsonify({'skill':find_skill})


@app.route('/feh/api/v1.0/assists', methods=['GET'])
def get_all_assists():
	''' Returns a json of all assists '''
	return jsonify({'assists':list(assists_col.find())})

@app.route('/feh/api/v1.0/assists/<int:assist_id>', methods=['GET'])
def get_assist(assist_id):
	''' Returns a assist matching specified id '''
	find_assist = list(assists_col.find({"_id":assist_id})) 
	if len(find_assist) == 0:
		abort(404)
	return jsonify({'assists':find_assist})



@app.route('/feh/api/v1.0/specials', methods=['GET'])
def get_all_specials():
	''' Returns a json of all specials '''
	return jsonify({'specials':list(special_col.find())})


@app.route('/feh/api/v1.0/specials/<int:special_id>', methods=['GET'])
def get_special(special_id):
	''' Returns a special matching specified id '''
	find_special = special_col.find({"_id":special_id})
	if len(find_special) ==0:
		abort(404)
	return jsonify({'specials':find_special})


@app.route('/feh/api/v1.0/accessories', methods=['GET'])
def get_all_accessories():
	''' Returns a json of all accessories '''
	return jsonify({'accessories': list(accessories_col.find())})

@app.route('/feh/api/v1.0/accessories/<int:accessory_id>', methods=['GET'])
def get_accessory(accessory_id):
	''' Returns a accessory matching specified id '''
	find_accessory = list(accessories_col.find({"_id" : accessory_id}))
	if len(find_accessory) == 0:
		abort(404)

	return jsonify({'accessory':find_accessory})







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



@app.route('/feh/api/v1.0/weapons', methods=['POST'])
def add_weapon():
	''' Adds a new weapon to the database '''

	if not request.json or not 'name' in request.json:
		abort(404)

	#gets the latest weapon id from the collection
	next_id = list(weapons_col.find({}, {'_id':1}).limit(1).sort('$natural',-1))

	new_weapon = {
		'id': next_id[0]['_id']+1,
		'name' : request.json['name'],
		'description': request.json.get('description', ""),
		'effective': request.json.get('effective', ""),
		'upgrade': request.json.get('upgrade', ""),
		'might': request.json.get('might', ""),
		'range': request.json.get('range', ""),
		'sp_cost': request.json.get('sp_cost', ""),
		'is_inheritable' : request.json.get('is_inheritable', ""),
		'heroes': request.json.get('heroes', "")

	}

	weapons_col.insert_one(new_weapon)
	
	return jsonify({'Added Weapon':new_weapon})


@app.route('/feh/api/v1.0/skills', methods=['POST'])
def add_skill():
	''' Add a new skill to the database '''

	if not request.json or not 'name' in request.json:
		abort(404)

	#gets the latest special id from the collection
	next_id = list(special_col.find({}, {'_id':1}).limit(1).sort('$natural',-1))


	new_skill = {
		'id' : next_id[0]['_id']+1,
		'name' : request.json['name'],
		'type': request.json.get('type'),
		'is_seal_avaliable':request.json.get('is_seal_avaliable'),
		'varients': request.json.get('varients'),
		'heroes':request.json.get('heroes')

	}

	skills_col.insert_one(new_skill)

	return jsonify({'Added Skill':new_skill})


@app.route('/feh/api/v1.0/assists', methods=['POST'])
def add_assist():
	''' Add a new assist to the database '''

	if not request.json or not 'name' in request.json:
		abort(404)

	#gets the latest assist id from the collection
	next_id = list(assist_col.find({}, {'_id':1}).limit(1).sort('$natural',-1))


	new_assist = {
		'id': next_id[0]['_id']+1,
		'name' : request.json['name'],
		'range':request.json.get('range'),
		'sp_cost':request.json.get('sp_cost'),
		'description': request.json.get('description'),
		'is_inheritable':request.json.get('is_inheritable'),
		'restriction': request.json.get('restriction'),
		'heroes':request.json.get('heroes')

	}

	assists_col.insert_one(new_assist)

	return jsonify({'Added Assist': new_assist})


@app.route('/feh/api/v1.0/specials', methods=['POST'])
def add_special():
	''' Add a new special to the database '''

	if not request.json or not 'name' in request.json:
		abort(404)

	#gets the latest special id from the collection
	next_id = list(special_col.find({}, {'_id':1}).limit(1).sort('$natural',-1))


	new_special = {
		'id': next_id[0]['_id']+1,
		'name': request.json['name'],
		'cooldown': request.json.get('cooldown'),
		'sp_cost': request.json.get('sp_cost'),
		'description':request.json.get('description'),
		'restriction': request.json.get('restriction'),
		'heroes': request.json.get('heroes')

	}

	special_col.insert_one(new_special)

	return jsonify({'Added Special' : new_special})


@app.route('/feh/api/v1.0/accessories', methods=['POST'])
def add_accessory():
	if not request.json or not 'name' in request.json:
		abort(404)

	#gets the latest special id from the collection
	current_id = list(special_col.find({}, {'_id':1}).limit(1).sort('$natural',-1))

	new_accessory = {
		'id': next_id[0]['_id']+1,
		'name' : request.json['name'],
		'type' : request.json.get('type'),
		'description' : request.json.get('description')
	}



##########################
''' DELETE FUNCTIONS '''
##########################

''' example curl function call 
curl -X "DELETE" http://127.0.0.1:5000/feh/api/v1.0/heroes/1
'''

@app.route('/feh/api/v1.0/heroes/<int:hero_id>', methods=['DELETE'])
def delete_hero(hero_id):
	''' Removes hero matching specified id '''
	remove_hero = heroes_col.delete_one({"_id": hero_id})

	if 	remove_hero.deleted_count == 0:
		abort(404)
	return jsonify({'Result':'True'})


@app.route('/feh/api/v1.0/weapons/<int:weapon_id>', methods=['DELETE'])
def delete_weapon(weapon_id):
	''' Removes weapon matching specified id '''
	remove_weapon = weapons_col.delete_one({"_id":weapon_id})
	if remove_weapon.deleted_count == 0:
		abort(404)

	return jsonify({'Result':'True'})

@app.route('/feh/api/v1.0/skills/<int:skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
	'''Removes skill matching specified id '''
	remove_skill = skills_col.delete_one({"_id":skill_id})
	if remove_skill.deleted_count == 0:
		abort(404)
	
	return jsonify({'Result':'True'})


@app.route('/feh/api/v1.0/assists/<int:assist_id>', methods=['DELETE'])
def delete_assist(assist_id):
	''' Remove assist matching specified id '''
	remove_assist = assists_col.delete_one({"_id":assist_id}) 
	if remove_assist.deleted_count == 0:
		abort(404)

	return jsonify({'Result':'True'})

@app.route('/feh/api/v1.0/specials/<int:special_id>', methods=['DELETE'])
def delete_special(special_id):
	''' Remove special matching specified id '''
	remove_special = special_col.delete_one({"_id":special_id})
	if remove_special.deleted_count == 0:
		abort(404)

	return jsonify({'Result':'True'})

@app.route('/feh/api/v1.0/accessories/<int:accessory_id>', methods=['DELETE'])
def delete_accessory(accessory_id):
	''' Remove accessory matching specified id '''
	remove_accessory = accessories_col.delete_one({"_id":accessory_id})
	if remove_accessory.deleted_count == 0:
		abort(404)
	return jsonify({'Result':'True'})


if __name__ == '__main__':
	#starts flask server
	app.run(debug=True)