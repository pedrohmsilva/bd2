from flask import Flask, request
from flask_restful import Resource, Api

import sys
sys.path.insert(0, '..')
from Connection import Connection
from util import Util

app = Flask(__name__)
api = Api(app)

class ListarCumprimentoPenas(Resource):
	def get(self):
		conn = Connection()

		command = (
			"select " + Util.formatQuery('cp', 'cumprimento_pena') + ", " +
			Util.formatQuery('cp.crime', 'crime') + ", " +
			Util.formatQuery('cp.prisioneiro', 'prisioneiro') +
			" from cumprimento_penas cp"
		)

		cumprimento_pena = conn.query(command)

		if (cumprimento_pena['success'] == False):
			return cumprimento_pena

		resultado = []
		for data in cumprimento_pena['data']:
			resultado.append(Util.formatResponse(data, cumprimento_pena['columns'], []))

		for i in range(len(resultado)):
			resultado[i]['codigo_penal'] = resultado[i]['crime.codigo_penal']
			resultado[i]['area_penal'] = resultado[i]['crime.area_penal']
			resultado[i]['descricao'] = resultado[i]['crime.descricao']
			resultado[i]['pena_unidade'] = resultado[i]['crime.pena_unidade']
			resultado[i]['pena_minima'] = resultado[i]['crime.pena_minima']
			resultado[i]['pena_maxima'] = resultado[i]['crime.pena_maxima']
			resultado[i]['cpf'] = resultado[i]['prisioneiro.cpf']
			resultado[i]['rg'] = resultado[i]['prisioneiro.rg']
			resultado[i]['nome'] = resultado[i]['prisioneiro.nome']
			resultado[i]['data_nascimento'] = resultado[i]['prisioneiro.data_nascimento']

			del resultado[i]['crime.codigo_penal']
			del resultado[i]['crime.area_penal']
			del resultado[i]['crime.descricao']
			del resultado[i]['crime.pena_unidade']
			del resultado[i]['crime.pena_minima']
			del resultado[i]['crime.pena_maxima']
			del resultado[i]['prisioneiro.cpf']
			del resultado[i]['prisioneiro.rg']
			del resultado[i]['prisioneiro.nome']
			del resultado[i]['prisioneiro.data_nascimento']

		return resultado

class BuscarCumprimentoPenas(Resource):
	def get(self):
		conn = Connection()

		codigo = str(request.args['codigo'])

		command = (
			"select " + Util.formatQuery('cp', 'cumprimento_pena') + ", " +
			Util.formatQuery('cp.crime', 'crime') + ", " +
			Util.formatQuery('cp.prisioneiro', 'prisioneiro') +
			" from cumprimento_penas cp" +
			" where cp.codigo = " + codigo
		)

		cumprimento_pena = conn.query(command)

		if (cumprimento_pena['success'] == False):
			return cumprimento_pena

		resultado = []
		for data in cumprimento_pena['data']:
			resultado.append(Util.formatResponse(data, cumprimento_pena['columns'], []))

		for i in range(len(resultado)):
			resultado[i]['codigo_penal'] = resultado[i]['crime.codigo_penal']
			resultado[i]['area_penal'] = resultado[i]['crime.area_penal']
			resultado[i]['descricao'] = resultado[i]['crime.descricao']
			resultado[i]['pena_unidade'] = resultado[i]['crime.pena_unidade']
			resultado[i]['pena_minima'] = resultado[i]['crime.pena_minima']
			resultado[i]['pena_maxima'] = resultado[i]['crime.pena_maxima']
			resultado[i]['cpf'] = resultado[i]['prisioneiro.cpf']
			resultado[i]['rg'] = resultado[i]['prisioneiro.rg']
			resultado[i]['nome'] = resultado[i]['prisioneiro.nome']
			resultado[i]['data_nascimento'] = resultado[i]['prisioneiro.data_nascimento']
			resultado[i]['data_inicio'] = resultado[i]['data_inicio'][:-9]
			resultado[i]['data_termino'] = resultado[i]['data_termino'][:-9]

			del resultado[i]['crime.codigo_penal']
			del resultado[i]['crime.area_penal']
			del resultado[i]['crime.descricao']
			del resultado[i]['crime.pena_unidade']
			del resultado[i]['crime.pena_minima']
			del resultado[i]['crime.pena_maxima']
			del resultado[i]['prisioneiro.cpf']
			del resultado[i]['prisioneiro.rg']
			del resultado[i]['prisioneiro.nome']
			del resultado[i]['prisioneiro.data_nascimento']

		return resultado

class CriarCumprimentoPenas(Resource):
	def post(self):
		conn = Connection()

		codigo = str(request.json['codigo'])
		prisioneiro = str(request.json['prisioneiro'])
		crime = str(request.json['crime'])
		data_inicio = "to_date('" + request.json['data_inicio'] + "', 'yyyy-mm-dd')"
		data_termino = "to_date('" + request.json['data_termino'] + "', 'yyyy-mm-dd')"
		
		command = (
			"insert into cumprimento_penas values (" +
				"Cumprimento_Pena_TY (" +
					codigo + ", " +
					"(select ref(p) from prisioneiros p where p.cpf = " + prisioneiro + "), " +
					"(select ref(c) from crimes c where c.codigo_penal = " + crime + "), " +
					data_inicio + ", " +
					data_termino +
				")" +
			")"
        )

		return conn.update(command)

class RemoverCumprimentoPenas(Resource):
	def post(self):
		conn = Connection()

		codigo = str(request.json['codigo'])

		command = (
			"delete from cumprimento_penas cp where" +
			" cp.codigo = " + codigo
		)

		return conn.update(command)

