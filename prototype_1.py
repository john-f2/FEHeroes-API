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


	}

]

weapons = [
	{
		'id': 1,
		'name':'Iron Sword',
		'might': 6,
		'range': 1,
		'sp_cost': 50,
		'heroes': ['Lucina: Future Witness']

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



	}


]

specials = [
	{
		'id':1,
		'name':'New Moon',
		'cooldown':3,
		'sp':100,
		'description':'Treats foe’s Def/Res as if reduced by 30% during combat',
		'restriction':['Staff'],
		'heroes':['Lucina: Future Witness']

	}


]


#default route, will fill in with actual home page
@app.route('/')
def index():
	return 'Fire Emblem Heroes API'


@app.route('/feh/api/v1.0/heroes', methods=['GET'])
def get_all_heroes():
	''' Returns a json of all heroes '''
	return jsonify({'heroes':heroes})

@app.route('/feh/api/v1.0/weapons', methods=['GET'])
def get_all_weapons():
	''' Returns a json of all weapons '''
	return jsonify({'weapons':weapons})

@app.route('/feh/api/v1.0/skills', methods=['GET'])
def get_all_skills():
	''' Returns a json of all skills '''
	return jsonify({'skills':skills})

@app.route('/feh/api/v1.0/specials', methods=['GET'])
def get_all_specials():
	''' Returns a json of all specials '''
	return jsonify({'specials':specials})


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'ERROR':'Not Found'}), 404)



if __name__ == '__main__':
	app.run(debug=True)

# * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

