from flask import Flask, request
from flask_restful import Resource, Api

import sys
sys.path.insert(0, '..')
from Connection import Connection
from util import Util

app = Flask(__name__)
api = Api(app)

class ListarCelas(Resource):
	def get(self):
		conn = Connection()
		command = ("select " + Util.formatQuery('c', 'cela') + ", " + Util.formatQuery('c.bloco', 'bloco') + ", " +
			Util.formatQuery('c.bloco.pavilhao', 'pavilhao') + ", " +
			Util.formatQuery('c.bloco.pavilhao.unidade_prisional', 'up') + ", " +
			Util.formatQuery('c.bloco.pavilhao.unidade_prisional.endereco', 'endereco') +
			" from celas c")

		celas = conn.query(command)

		if (celas['success'] == False):
			return celas

		resultado = []
		for data in celas['data']:
			resultado.append(Util.formatResponse(data, celas['columns'], ['bloco', 'pavilhao', 'unidade_prisional', 'endereco']))

		return resultado

class BuscarCelas(Resource):
	def get(self):
		conn = Connection()

		codigo_unidade = str(request.args['fk_codigo_unidade'])
		numero_pavilhao = str(request.args['fk_numero_pavilhao'])
		numero_bloco = str(request.args['fk_numero_bloco'])
		codigo_cela = str(request.args['codigo'])

		command = ("select " + Util.formatQuery('c', 'cela') + ", " + Util.formatQuery('c.bloco', 'bloco') + ", " +
			Util.formatQuery('c.bloco.pavilhao', 'pavilhao') + ", " +
			Util.formatQuery('c.bloco.pavilhao.unidade_prisional', 'up') + ", " +
			Util.formatQuery('c.bloco.pavilhao.unidade_prisional.endereco', 'endereco') +
			" from celas c where " +
				"c.bloco.pavilhao.unidade_prisional.codigo = " + codigo_unidade + " and " +
				"c.bloco.pavilhao.numero = " + numero_pavilhao + " and " +
				"c.bloco.numero = " + numero_bloco + " and " +
				"c.codigo = " + codigo_cela
		)

		celas = conn.query(command)

		if (celas['success'] == False):
			return celas

		resultado = []
		for data in celas['data']:
			resultado.append(Util.formatResponse(data, celas['columns'], ['blcoo', 'pavilhao', 'unidade_prisional', 'endereco']))

		return resultado


class CriarCelas(Resource):
	def post(self):
		conn = Connection()

		codigo_unidade = str(request.json['fk_codigo_unidade'])
		numero_pavilhao = str(request.json['fk_numero_pavilhao'])
		numero_bloco = str(request.json['fk_numero_bloco'])
		codigo_cela = str(request.json['codigo'])
		capacidade = str(request.json['capacidade'])
		tipo = Util.formatString(request.json['tipo'])

		command = (
			"insert into celas values (" +
				"(" +
					"select ref(b) from blocos b where " +
					"b.numero = " + numero_bloco + " and " +
					"b.pavilhao.numero = " + numero_pavilhao + " and " +
					"b.pavilhao.unidade_prisional.codigo = " + codigo_unidade +
				"), " +
				codigo_cela + ", " +
				capacidade + ", " +
				tipo +
			")"
        )

		return conn.update(command)

class AlterarCelas(Resource):
	def post(self):
		conn = Connection()

		codigo_unidade = str(request.json['fk_codigo_unidade'])
		numero_pavilhao = str(request.json['fk_numero_pavilhao'])
		numero_bloco = str(request.json['fk_numero_bloco'])
		codigo_cela = str(request.json['codigo'])

		capacidade = str(request.json['capacidade'])
		tipo = Util.formatString(request.json['tipo'])

		command = (
			"update celas c set " +
				"c.capacidade = " + capacidade + ", " +
				"c.tipo = " + tipo +
			" where " +
				"c.codigo = " + codigo_cela + " and " +
				"c.bloco.numero = " + numero_bloco + " and " +
				"c.bloco.pavilhao.numero = " + numero_pavilhao + " and " +
				"c.bloco.pavilhao.unidade_prisional.codigo = " + codigo_unidade
		)

		return conn.update(command)

class RemoverCelas(Resource):
	def post(self):
		conn = Connection()

		codigo_unidade = str(request.json['fk_codigo_unidade'])
		numero_pavilhao = str(request.json['fk_numero_pavilhao'])
		numero_bloco = str(request.json['fk_numero_bloco'])
		codigo_cela = str(request.json['codigo'])

		command = (
			"delete from celas c where" +
			" c.codigo = " + codigo_cela + " and"
			" c.bloco.numero = " + numero_bloco + " and"
			" c.bloco.pavilhao.numero = " + numero_pavilhao + " and"
			" c.bloco.pavilhao.unidade_prisional.codigo = " + codigo_unidade
		)

		return conn.update(command)

