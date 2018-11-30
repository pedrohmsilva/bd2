from flask import Flask, request
from flask_restful import Resource, Api

import sys
sys.path.insert(0, '..')
from Connection import Connection
from util import Util

app = Flask(__name__)
api = Api(app)

class ListarBlocos(Resource):
	def get(self):
		conn = Connection()
		command = ("select " + Util.formatQuery('b', 'bloco') + ", " + Util.formatQuery('b.pavilhao', 'pavilhao') + ", " +
			Util.formatQuery('b.pavilhao.unidade_prisional', 'up') + ", " + Util.formatQuery('b.pavilhao.unidade_prisional.endereco', 'endereco') +
			" from blocos b")

		blocos = conn.query(command)

		if (blocos['success'] == False):
			return blocos

		resultado = []
		for data in blocos['data']:
			resultado.append(Util.formatResponse(data, blocos['columns'], ['pavilhao', 'unidade_prisional', 'endereco']))

		for i in range(len(resultado)):
			resultado[i]['fk_numero_pavilhao'] = resultado[i]['.numero']
			resultado[i]['funcao_pavilhao'] = resultado[i]['.funcao']
			resultado[i]['fk_codigo_unidade'] = resultado[i]['..codigo']
			resultado[i]['nome_unidade'] = resultado[i]['..nome']
			resultado[i]['tipo_logradouro'] = resultado[i]['...tipo_logadouro']
			resultado[i]['logradouro'] = resultado[i]['...logradouro']
			resultado[i]['num'] = resultado[i]['...numero']
			resultado[i]['bairro'] = resultado[i]['...bairro']
			resultado[i]['cidade'] = resultado[i]['...cidade']
			resultado[i]['uf'] = resultado[i]['...uf']
			resultado[i]['cep'] = resultado[i]['...cep']

			del resultado[i]['.numero']
			del resultado[i]['.funcao']
			del resultado[i]['..codigo']
			del resultado[i]['..nome']
			del resultado[i]['...tipo_logadouro']
			del resultado[i]['...logradouro']
			del resultado[i]['...numero']
			del resultado[i]['...bairro']
			del resultado[i]['...cidade']
			del resultado[i]['...uf']
			del resultado[i]['...cep']

		return resultado

class BuscarBlocos(Resource):
	def get(self):
		conn = Connection()

		numero_pavilhao = str(request.args['fk_numero_pavilhao'])
		numero_bloco = str(request.args['numero'])

		command = (
			"select " + Util.formatQuery('b', 'bloco') + ", " + Util.formatQuery('b.pavilhao', 'pavilhao') + ", " +
			Util.formatQuery('b.pavilhao.unidade_prisional', 'up') + ", " + Util.formatQuery('b.pavilhao.unidade_prisional.endereco', 'endereco') +
			" from blocos b where " +
			"b.numero = " + numero_bloco + " and " +
			"b.pavilhao.numero = " + numero_pavilhao
		)

		blocos = conn.query(command)

		if (blocos['success'] == False):
			return blocos

		resultado = []
		for data in blocos['data']:
			resultado.append(Util.formatResponse(data, blocos['columns'], ['pavilhao', 'unidade_prisional', 'endereco']))

		for i in range(len(resultado)):
			resultado[i]['fk_numero_pavilhao'] = resultado[i]['.numero']
			resultado[i]['funcao_pavilhao'] = resultado[i]['.funcao']
			resultado[i]['codigo_unidade'] = resultado[i]['..codigo']
			resultado[i]['nome_unidade'] = resultado[i]['..nome']
			resultado[i]['tipo_logradouro'] = resultado[i]['...tipo_logadouro']
			resultado[i]['logradouro'] = resultado[i]['...logradouro']
			resultado[i]['num'] = resultado[i]['...numero']
			resultado[i]['bairro'] = resultado[i]['...bairro']
			resultado[i]['cidade'] = resultado[i]['...cidade']
			resultado[i]['uf'] = resultado[i]['...uf']
			resultado[i]['cep'] = resultado[i]['...cep']

			del resultado[i]['.numero']
			del resultado[i]['.funcao']
			del resultado[i]['..codigo']
			del resultado[i]['..nome']
			del resultado[i]['...tipo_logadouro']
			del resultado[i]['...logradouro']
			del resultado[i]['...numero']
			del resultado[i]['...bairro']
			del resultado[i]['...cidade']
			del resultado[i]['...uf']
			del resultado[i]['...cep']

		return resultado


class CriarBlocos(Resource):
	def post(self):
		conn = Connection()

		numero_pavilhao = str(request.json['fk_numero_pavilhao'])
		codigo_unidade = str(request.json['fk_codigo_unidade'])
		numero_bloco = str(request.json['numero'])
		andar_pavilhao = str(request.json['andar'])

		command = (
			"insert into blocos values (" +
				"(" +
					"select ref(p) from pavilhoes p where " +
					"p.unidade_prisional.codigo = " + codigo_unidade + " and " +
					"p.numero = " + numero_pavilhao + 
				"), " +
				numero_bloco + ", " +
				andar_pavilhao +
			")"
        )

		return conn.update(command)

class AlterarBlocos(Resource):
	def post(self):
		conn = Connection()

		numero_bloco = str(request.json['numero'])
		numero_pavilhao = str(request.json['fk_numero_pavilhao'])
		codigo_unidade = str(request.json['fk_codigo_unidade'])
		andar = str(request.json['andar'])

		command = (
			"update blocos b set " +
				"b.andar = " + andar +
			" where " +
				"b.numero = " + numero_bloco + " and " +
				"b.pavilhao.numero = " + numero_pavilhao + " and " +
				"b.pavilhao.unidade_prisional.codigo = " + codigo_unidade
		)

		return conn.update(command)

class RemoverBlocos(Resource):
	def post(self):
		conn = Connection()

		numero_bloco = str(request.json['numero'])
		numero_pavilhao = str(request.json['fk_numero_pavilhao'])
		codigo_unidade = str(request.json['fk_codigo_unidade'])

		command = (
			"delete from blocos b where" +
			" b.numero = " + numero_bloco + " and"
			" b.pavilhao.numero = " + numero_pavilhao + " and"
			" b.pavilhao.unidade_prisional.codigo = " + codigo_unidade
		)

		return conn.update(command)