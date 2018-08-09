#!myvenv/bin/python
from flask import Flask

app = Flask(__name__)

'''
build and run command 
chmod a+x <file>.py
./<file>.py

'''

#index path
@app.route("/")
def hello_test():
	''' Testing to see if Flask is working '''
	return "Flask Test, Hello World!"


if __name__ == '__main__':
	app.run(debug=True)



