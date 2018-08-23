#!myvenv/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

'''

Prototype 1 for Fire Emeblem Heroes API

Focus - To set up the API and create a template for data model 


@author john-f2


'''

app = Flask(__name__)



#initial template data model for api
#not intended for the final api
#will be replaced with a database later (mongodb)
heroes = [
	{
		#temporary ID number
		'id':1,
		'name':'Lucina: Future Witness',
		'description': 'A princess and daughter of Chrom who traveled to her past to prevent apocalypse',
		'rarities':[5],
		'w_type':'Sword',
		'm_type':'Infantry',
		'weapons':['Iron Sword','Steel Sword','Silver Sword','Falchion'],
		'assists':[],
		'specials':['New Moon', 'Luna', 'Aether'],
		'passives':{'A':['Defiant Spd 1', 'Defiant Spd 2', 'Defiant Spd 3'], 'B':[],
		'C':['Spur Atk 1','Spur Atk 2', 'Spur Atk 3']},
		'stats': {'lvl_1':{'HP':[18,19,20],'ATK':[7,8,9],'SPD':[9,10,11],'DEF':[5,6,7],'RES':[3,4,5]},
		'lvl_40':{'HP':[40,43,46],'ATK':[31,34,37],'SPD':[33,36,39],'DEF':[22,25,29],'RES':[16,19,22]}},
		'growth_points':{'HP':7,'ATK':8,'SPD':8,'DEF':5,'RES':3}


	},
	{
		'id':2,
		'name':'Azura: Lady of the Lake',
		'description': 'An enchanting princess raised in Hoshido who sings in battle to help her allies.',
		'rarities':[5],
		'w_type':'Lance',
		'm_type':'Infantry',
		'weapons':['Iron Lance','Steel Lance','Sapphire Lance','Sapphire Lance+'],
		'assists':['Sing'],
		'specials':[],
		'passives':{'A':['Speed +1', 'Speed +2', 'Speed +3'], 'B':[],
		'C':['Fortify Res 1','Fortify Res 2', 'Fortify Res 3']},
		'stats': {'lvl_1':{'HP':[16,17,18],'ATK':[4,5,6],'SPD':[6,7,8],'DEF':[3,4,5],'RES':[5,6,7]},
			'lvl_40':{'HP':[33,36,40],'ATK':[28,31,34],'SPD':[30,33,36],'DEF':[18,21,24],'RES':[24,28,31]}},
		'growth_points':{'HP':5,'ATK':8,'SPD':8,'DEF':4,'RES':6}


	}

]

weapons = [
	{
		'id': 1,
		'name':'Iron Sword',
		'description':'',
		'effective':[],
		'upgrade':{},
		'might': 6,
		'range': 1,
		'sp_cost': 50,
		'is_inheritable' : True,
		'heroes': ['Lucina: Future Witness']

	},
	{
		'id': 2,
		'name':'Falchion',
		'description':'Effective against dragon foes. At the start of every third turn, restores 10 HP.',
		'effective':['dragon'],
		'upgrade':{'S1':{'stat':['+3 HP'], 'description':'If unit is adjacent to an ally, grants Atk/Spd/Def/Res+4 during combat.', 'cost':{'SP':400, 'medal': 500, 'dew':200}},
			'atk':{'stat':['+5 HP','+2 Mt'], 'description':'', 'cost':{'SP':400, 'medal': 500, 'dew':200}},
			'spd':{'stat':['+5 HP','+3 Spd'], 'description':'', 'cost':{'SP':400, 'medal': 500, 'dew':200}},
			'def':{'stat':['+5 HP','+4 Def'], 'description':'', 'cost':{'SP':400, 'medal': 500, 'dew':200}},
			'res':{'stat':['+5 HP','+4 Res'], 'description':'', 'cost':{'SP':400, 'medal': 500, 'dew':200}}},
			'might': 16,
		'range': 1,
		'sp_cost': 400,
		'is_inheritable':False,
		'heroes': ['Lucina: Future Witness']

	},
	{
		'id': 3,
		'name':'Iron Lance',
		'description':'',
		'effective':[],
		'upgrade':{},
		'might': 6,
		'range': 1,
		'sp_cost': 50,
		'is_inheritable' : True,
		'heroes': ['Azura: Lady of the Lake']

	}

]

skills = [
	{
		'id': 1,
		'name': 'Defiant Spd',
		'type': 'A',
		'is_seal_avaliable' : True,
		'varients': {'1': {'SP':40, 'description':'At start of turn, if unit\'s HP <= 50%, grants Spd+3 for 1 turn'},
			'2':{'SP':80, 'description':'At start of turn, if unit\'s HP <= 50%, grants Spd+5 for 1 turn'},
			'3':{'SP':160, 'description':'At start of turn, if unit\'s HP <= 50%, grants Spd+7 for 1 turn'}},
		'heroes':['Lucina: Future Witness']
	},
	{
		'id': 2,
		'name': 'Fortify Resistance',
		'type': 'C',
		'is_seal_avaliable':True,
		'varients': {'1': {'SP':50, 'description':'At start of turn, grants Res+2 to adjacent allies for 1 turn.'},
			'2':{'SP':100, 'description':'At start of turn, grants Res+3 to adjacent allies for 1 turn.'},
			'3':{'SP':200, 'description':'At start of turn, grants Res+4 to adjacent allies for 1 turn.'}},
		'heroes':['Azura: Lady of the Lake']
	},


]

assists = [
	{
		'id':1,
		'name':'Sing',
		'range':1,
		'sp_cost':150,
		'description':'Grants another action to target ally. (Cannot target an ally with Sing or Dance.)',
		'is_inheritable':False,
		'restriction':['Staff'],
		'heroes':['Azura: Lady of the Lake']

	}


]

specials = [
	{
		'id':1,
		'name':'New Moon',
		'cooldown':3,
		'sp_cost':100,
		'description':'Treats foe’s Def/Res as if reduced by 30% during combat',
		'restriction':['Staff'],
		'heroes':['Lucina: Future Witness']

	}


]


#default route, will fill in with actual home page
@app.route('/')
def index():
	return 'Fire Emblem Heroes API'


#######################
''' GET FUNCTIONS '''
#######################

@app.route('/feh/api/v1.0/heroes', methods=['GET'])
def get_all_heroes():
	''' Returns a json of all heroes '''
	return jsonify({'heroes':heroes})



@app.route('/feh/api/v1.0/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
	''' Returns a hero with matching id '''
	hero = [hero for hero in heroes if hero['id'] == hero_id]
	if len(hero) == 0:
		#if id not found return 404 error
		abort(404)
	return jsonify({'heroes':hero[0]}) 



@app.route('/feh/api/v1.0/weapons', methods=['GET'])
def get_all_weapons():
	''' Returns a json of all weapons '''
	return jsonify({'weapons':weapons})

@app.route('/feh/api/v1.0/weapons/<int:weapon_id>', methods=['GET'])
def get_weapon(weapon_id):
	'''Returns a weapon with matching id '''
	weapon = [weapon for weapon in weapons if weapon['id'] == weapon_id]
	if len(weapon) == 0:
		abort(404)
	return jsonify({'weapons':weapon[0]})



@app.route('/feh/api/v1.0/skills', methods=['GET'])
def get_all_skills():
	''' Returns a json of all skills '''
	return jsonify({'skills':skills})

@app.route('/feh/api/v1.0/skills/<int:skill_id>', methods=['GET'])
def get_skill(skill_id):
	'''Returns a weapon with matching id '''
	skill = [skill for skill in skills if skill['id'] == skill_id]
	if len(skill) == 0:
		abort(404)
	return jsonify({'skill':skill[0]})


@app.route('/feh/api/v1.0/assists', methods=['GET'])
def get_all_assists():
	''' Returns a json of all assists '''
	return jsonify({'assists':assists})

@app.route('/feh/api/v1.0/assists/<int:assist_id>', methods=['GET'])
def get_assist(assist_id):
	''' Returns a assist matching specified id '''
	assist = [assist for assist in assists if assist['id'] == assist_id]
	if len(assist) == 0:
		abort(404)
	return jsonify({'assists':assists[0]})



@app.route('/feh/api/v1.0/specials', methods=['GET'])
def get_all_specials():
	''' Returns a json of all specials '''
	return jsonify({'specials':specials})


@app.route('/feh/api/v1.0/specials/<int:special_id>', methods=['GET'])
def get_special(special_id):
	''' Returns a special matching specified id '''
	special = [special for special in specials if special['id'] == special_id ]
	if len(special) ==0:
		abort(404)
	return jsonify({'specials':special[0]})



########################
''' POST FUNCTIONS ''' 
########################


@app.route('/feh/api/v1.0/heroes', methods=['POST'])
def add_hero():
	''' Adds a new hero to the database '''

	#if the reqest is not in json format or does not have a 'name' value
	#then abort 
	if not request.json or not 'name' in request.json:
		abort(404)
	new_hero = {
		'id' : heroes[-1]['id'] + 1,
		'name': request.json['name'],
		'description': request.json.get('description', ""), 
		'rarities': request.json.get('rarities', ""),
		'w_type': request.json.get('w_type', ""),
		'm_type': request.json.get('m_type', ""),
		'weapons': request.json.get('weapons', ""),
		'assists': request.json.get('assists', ""),
		'specials': request.json.get('specials', ""),
		'passives': request.json.get('passives', "") ,
		'stats': request.json.get('stats', "") ,
		'growth_points': request.json.get('growth_points', "")

	}

	heroes.append(new_hero)

	#returns back the json of the new hero and a 201 status code meaning "created"
	return jsonify({'Added Hero': new_hero}), 201


@app.route('/feh/api/v1.0/weapons', methods=['POST'])
def add_weapon():
	''' Adds a new weapon to the database '''

	if not request.json or not 'name' in request.json:
		abort(404)

	new_weapon = {
		'id': weapons[-1]['id'] + 1,
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

	weapons.append(new_weapon)
	
	return jsonify({'Added Weapon':new_weapon})


@app.route('/feh/api/v1.0/skills', methods=['POST'])
def add_skill():
	''' Add a new skill to the database '''

	if not request.json or not 'name' in request.json:
		abort(404)

	new_skill = {
		'id' : skills[-1]['id'] + 1,
		'name' : request.json['name'],
		'type': request.json.get('type'),
		'is_seal_avaliable':request.json.get('is_seal_avaliable'),
		'varients': request.json.get('varients'),
		'heroes':request.json.get('heroes')

	}

	skills.append(new_skill)

	return jsonify({'Added Skill':new_skill})


@app.route('/feh/api/v1.0/assists', methods=['POST'])
def add_assist():
	''' Add a new assist to the database '''

	if not request.json or not 'name' in request.json:
		abort(404)

	new_assist = {
		'id': assists[-1]['id'] + 1,
		'name' : request.json['name'],
		'range':request.json.get('range'),
		'sp_cost':request.json.get('sp_cost'),
		'description': request.json.get('description'),
		'is_inheritable':request.json.get('is_inheritable'),
		'restriction': request.json.get('restriction'),
		'heroes':request.json.get('heroes')

	}

	assists.append(new_assist)

	return jsonify({'Added Assist': new_assist})


@app.route('/feh/api/v1.0/specials', methods=['POST'])
def add_special():
	''' Add a new special to the database '''

	if not request.json or not 'name' in request.json:
		abort(404)

	new_special = {
		'id': specials[-1]['id'] +1,
		'name': request.json['name'],
		'cooldown': request.json.get('cooldown'),
		'sp_cost': request.json.get('sp_cost'),
		'description':request.json.get('description'),
		'restriction': request.json.get('restriction'),
		'heroes': request.json.get('heroes')

	}

	specials.append(new_special)

	return jsonify({'Added Special' : new_special})



##########################
''' UPDATE FUNCTIONS '''
##########################


@app.route('/feh/api/v1.0/heroes/<int:hero_id>', methods=['PUT'])
def update_hero(hero_id):
	''' Updates specified hero's information, currently uses hero id, 
	will probably change it to hero name later '''

	#gets the hero matching parameter id 
	hero = [hero for hero in heroes if hero['id'] == hero_id]

	#checks if given data is in correct format 
	if len(hero) == 0:
		abort(404)
	if not request.json:
		abort(400)
	if 'name' in request.json and type(request.json['name']) is not str:
		abort(400)
	if 'description' in request.json and type(request.json['description']) is not str:
		abort(400)
	if 'rarities' in request.json and type(request.json['rarities']) is not list:
		abort(400)
	if 'w_type' in request.json and type(request.json['w_type']) is not str:
		abort(400)
	if 'm_type' in request.json and type(request.json['m_type']) is not str:
		abort(400)
	if 'weapons' in request.json and type(request.json['weapons']) is not list:
		abort(400)
	if 'assists' in request.json and type(request.json['assists']) is not list:
		abort(400)
	if 'passives' in request.json and type(request.json['passives']) is not dict:
		abort(400)
	if 'stats' in request.json and type(request.json['stats']) is not dict:
		abort(400)
	if 'growth_points' in request.json and type(request.json['growth_points']) is not dict:
		abort(400)

	#sets the new hero's data to database
	hero[0]['name'] = request.json.get('name', hero[0]['name'])
	hero[0]['description'] = request.json.get('description', hero[0]['description'])
	hero[0]['rarities'] = request.json.get('rarities', hero[0]['rarities'])
	hero[0]['w_type'] = request.json.get('w_type', hero[0]['w_type'])
	hero[0]['m_type'] = request.json.get('m_type', hero[0]['m_type'])
	hero[0]['weapons'] = request.json.get('weapons', hero[0]['weapons'])
	hero[0]['assists'] = request.json.get('assists', hero[0]['assists'])
	hero[0]['passives'] = request.json.get('passives', hero[0]['passives'])
	hero[0]['stats'] = request.json.get('stats', hero[0]['stats'])
	hero[0]['growth_points'] = request.json.get('growth_points', hero[0]['growth_points'])

	return jsonify({'Updated hero':hero[0] })


@app.route('/feh/api/v1.0/weapons/<int:weapon_id>', methods=['PUT'])
def update_weapon(weapon_id):
	''' Updates specified weapon '''
	weapon = [weapon for weapon in weapons if weapon['id'] == weapon_id]

	#checks if given json is correct
	if len(weapon) == 0:
		abort(404)
	if not request.json:
		abort(400)
	if 'name' in request.json and type(request.json['name']) is not str:
		abort(400)
	if 'description' in request.json and type(request.json['description']) is not str:
		abort(400)
	if 'effective' in request.json and type(request.json['effective']) is not list:
		abort(400)
	if 'upgrade' in request.json and type(request.json['upgrade']) is not dict:
		abort(400)
	if 'might' in request.json and type(request.json['might']) is not int:
		abort(400)
	if 'range' in request.json and type(request.json['range']) is not int:
		abort(400)
	if 'is_inheritable' in request.json and type(request.json['is_inheritable']) is not bool:
		abort(400)
	if 'sp_cost' in request.json and type(request.json['sp_cost']) is not int:
		abort(400)
	if 'heroes' in request.json and type(request.json['heroes']) is not list:
		abort(400)

	weapon[0]['name'] = request.json.get('name', weapon[0]['name'])
	weapon[0]['description'] = request.json.get('description', weapon[0]['description'])
	weapon[0]['effective'] = request.json.get('effective', weapon[0]['effective'])
	weapon[0]['upgrade'] = request.json.get('upgrade', weapon[0]['upgrade'])
	weapon[0]['might'] = request.json.get('might', weapon[0]['might'])
	weapon[0]['is_inheritable'] = request.json.get('is_inheritable', weapon[0]['is_inheritable'])
	weapon[0]['range'] = request.json.get('range', weapon[0]['range'])
	weapon[0]['sp_cost'] = request.json.get('sp_cost', weapon[0]['sp_cost'])
	weapon[0]['heroes'] = request.json.get('heroes', weapon[0]['heroes'])

	return jsonify({"Updated hero":weapon[0]})


@app.route('/feh/api/v1.0/skills/<int:skill_id>', methods=['PUT'])
def update_skill(skill_id):
	''' Updates specified skill '''

	skill = [skill for skill in skills if skill['id'] == skill_id]
	if len(skill) == 0:
		abort(404)
	if not request.json:
		abort(400)
	if 'name' in request.json and type(request.json['name']) is not str:
		abort(400)
	if 'type' in request.json and type(request.json['type']) is not str:
		abort(400)
	if 'is_seal_avaliable' in request.json and type(request.json['is_seal_avaliable']) is not bool:
		abort(400)
	if 'varients' in request.json and type(request.json['varients']) is not dict:
		abort(400)
	if 'heroes' in request.json and type(request.json['heroes']) is not list:
		abort(400)

	skill[0]['name'] = request.json.get('name', skill[0]['name'])
	skill[0]['type'] = request.json.get('type', skill[0]['type'])
	skill[0]['is_seal_avaliable'] = request.json.get('is_seal_avaliable', skill[0]['is_seal_avaliable'])
	skill[0]['varients'] = request.json.get('varients', skill[0]['varients'])
	skill[0]['heroes'] = request.json.get('heroes', skill[0]['heroes'])

	return jsonify({'Updated Skill' : skill[0]})














##########################
''' DELETE FUNCTIONS '''
##########################

''' example curl function call 
curl -X "DELETE" http://127.0.0.1:5000/feh/api/v1.0/heroes/1
'''

@app.route('/feh/api/v1.0/heroes/<int:hero_id>', methods=['DELETE'])
def delete_hero(hero_id):
	''' Removes hero matching specified id '''
	remove_hero = [hero for hero in heroes if hero['id'] == hero_id]
	if len(remove_hero) == 0:
		abort(404)
	heroes.remove(remove_hero[0])
	return jsonify({'Result':'True'})


@app.route('/feh/api/v1.0/weapons/<int:weapon_id>', methods=['DELETE'])
def delete_weapon(weapon_id):
	''' Removes weapon matching specified id '''
	remove_weapon = [weapon for weapon in weapons if weapon['id'] == weapon_id]
	if len(remove_weapon) == 0:
		abort(404)
	weapons.remove(remove_weapon[0])
	return jsonify({'Result':'True'})

@app.route('/feh/api/v1.0/skills/<int:skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
	'''Removes skill matching specified id '''
	skill = [skill for skill in skills if skill['id'] == skill_id]
	if len(skill) == 0:
		abort(404)
	skills.remove(skill[0])
	return jsonify({'Result':'True'})


@app.route('/feh/api/v1.0/assists/<int:assist_id>', methods=['DELETE'])
def delete_assist(assist_id):
	''' Remove assist matching specified id '''
	assist = [assist for assist in assists if assist['id'] == assist_id]
	if len(assist) == 0:
		abort(404)
	assist.remove(assist[0])
	return jsonify({'Result':True})

@app.route('/feh/api/v1.0/specials/<int:special_id>', methods=['DELETE'])
def delete_special(special_id):
	''' Remove special matching specified id '''
	special = [special for special in specials if special['id'] == special_id]
	if len(special) == 0:
		abort(404)
	speials.remove(special[0])
	return jsonify({'Result':True})










@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'ERROR':'Not Found'}), 404)



if __name__ == '__main__':
	app.run(debug=True)

# * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

