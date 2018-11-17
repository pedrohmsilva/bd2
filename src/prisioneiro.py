from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Prisioneiro(Resource):
	def get(self, num):
		return "Buscando prisioneiro " + str(num)

	def post(self):
		return "Adicionando prisioneiro..."