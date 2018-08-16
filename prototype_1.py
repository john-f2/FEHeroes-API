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
		'heroes': ['Azura: Lady of the Lake']

	}

]

skills = [
	{
		'id': 1,
		'name': 'Defiant Spd',
		'type': 'A',
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


''' GET FUNCTIONS '''

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



''' DELETE FUNCTIONS '''

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









@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'ERROR':'Not Found'}), 404)



if __name__ == '__main__':
	app.run(debug=True)

# * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

