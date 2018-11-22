from flask import Flask, request
from flask_restful import Resource, Api

import sys
sys.path.insert(0, '..')
from Connection import Connection
from util import Util

app = Flask(__name__)
api = Api(app)

class ListarCrimes(Resource):
	def get(self):
		conn = Connection()
		command = ("select " + Util.formatQuery('c', 'crime') +	" from crimes c")

		crimes = conn.query(command)

		if (crimes['success'] == False):
			return crimes

		resultado = []
		for data in crimes['data']:
			resultado.append(Util.formatResponse(data, crimes['columns'], []))

		return resultado

class BuscarCrimes(Resource):
	def get(self):
		conn = Connection()

		codigo_penal = str(request.args['codigo_penal'])

		command = ("select " + Util.formatQuery('c', 'crime') +
			" from crimes c where " +
				"c.codigo_penal = " + codigo_penal
		)

		codigo_penal = conn.query(command)

		if (codigo_penal['success'] == False):
			return codigo_penal

		resultado = []
		for data in codigo_penal['data']:
			resultado.append(Util.formatResponse(data, codigo_penal['columns'], []))

		return resultado


class CriarCrimes(Resource):
	def post(self):
		conn = Connection()

		codigo_penal = str(request.json['codigo_penal'])
		area_penal = Util.formatString(request.json['area_penal'])
		descricao = Util.formatString(request.json['descricao'])
		pena_unidade = Util.formatString(request.json['pena_unidade'])
		pena_minima = str(request.json['pena_minima'])
		pena_maxima = str(request.json['pena_maxima'])
		
		command = (
			"insert into crimes values (" +
				"Crime_TY (" +
					codigo_penal + ", " +
					area_penal + ", " +
					descricao + ", " +
					pena_unidade + ", " +
					pena_minima + ", " +
					pena_maxima +
				")" +
			")"
        )

		return conn.update(command)

class AlterarCrimes(Resource):
	def post(self):
		conn = Connection()

		codigo_penal = str(request.json['codigo_penal'])

		area_penal = Util.formatString(request.json['area_penal'])
		descricao = Util.formatString(request.json['descricao'])
		pena_unidade = Util.formatString(request.json['pena_unidade'])
		pena_minima = str(request.json['pena_minima'])
		pena_maxima = str(request.json['pena_maxima'])

		command = (
			"update crimes c set " +
				"c.area_penal = " + area_penal + ", " +
				"c.descricao = " + descricao + ", " +
				"c.pena_unidade = " + pena_unidade + ", " +
				"c.pena_minima = " + pena_minima + ", " +
				"c.pena_maxima = " + pena_maxima +
			" where " +
				"c.codigo_penal = " + codigo_penal
		)

		return conn.update(command)

class RemoverCrimes(Resource):
	def post(self):
		conn = Connection()

		codigo_penal = str(request.json['codigo_penal'])

		command = (
			"delete from crimes c where" +
			" c.codigo_penal = " + codigo_penal
		)

		return conn.update(command)

