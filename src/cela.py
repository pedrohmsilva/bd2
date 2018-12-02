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

		for i in range(len(resultado)):
			resultado[i]['numero_bloco'] = resultado[i]['.numero']
			resultado[i]['andar_bloco'] = resultado[i]['.andar']
			resultado[i]['numero_pavilhao'] = resultado[i]['..numero']
			resultado[i]['funcao_pavilhao'] = resultado[i]['..funcao']
			resultado[i]['codigo_unidade'] = resultado[i]['...codigo']
			resultado[i]['nome'] = resultado[i]['...nome']
			resultado[i]['tipo_logradouro'] = resultado[i]['....tipo_logadouro']
			resultado[i]['logradouro'] = resultado[i]['....logradouro']
			resultado[i]['num'] = resultado[i]['....numero']
			resultado[i]['bairro'] = resultado[i]['....bairro']
			resultado[i]['cidade'] = resultado[i]['....cidade']
			resultado[i]['uf'] = resultado[i]['....uf']
			resultado[i]['cep'] = resultado[i]['....cep']

			del resultado[i]['.numero']
			del resultado[i]['.andar']
			del resultado[i]['..numero']
			del resultado[i]['..funcao']
			del resultado[i]['...codigo']
			del resultado[i]['...nome']
			del resultado[i]['....tipo_logadouro']
			del resultado[i]['....logradouro']
			del resultado[i]['....numero']
			del resultado[i]['....bairro']
			del resultado[i]['....cidade']
			del resultado[i]['....uf']
			del resultado[i]['....cep']

		return resultado

class BuscarCelas(Resource):
	def get(self):
		conn = Connection()

		codigo_cela = str(request.args['codigo'])

		command = ("select " + Util.formatQuery('c', 'cela') + ", " + Util.formatQuery('c.bloco', 'bloco') + ", " +
			Util.formatQuery('c.bloco.pavilhao', 'pavilhao') + ", " +
			Util.formatQuery('c.bloco.pavilhao.unidade_prisional', 'up') + ", " +
			Util.formatQuery('c.bloco.pavilhao.unidade_prisional.endereco', 'endereco') +
			" from celas c where " +
				"c.codigo = " + codigo_cela
		)

		celas = conn.query(command)

		if (celas['success'] == False):
			return celas

		resultado = []
		for data in celas['data']:
			resultado.append(Util.formatResponse(data, celas['columns'], ['bloco', 'pavilhao', 'unidade_prisional', 'endereco']))

		for i in range(len(resultado)):
			resultado[i]['quantidade_max'] = resultado[i]['capacidade']
			resultado[i]['fk_numero_bloco'] = resultado[i]['.numero']
			resultado[i]['numero_bloco'] = resultado[i]['.numero']
			resultado[i]['andar_bloco'] = resultado[i]['.andar']
			resultado[i]['fk_numero_pavilhao'] = resultado[i]['..numero']
			resultado[i]['numero_pavilhao'] = resultado[i]['..numero']
			resultado[i]['codigo_unidade'] = resultado[i]['...codigo']
			resultado[i]['nome'] = resultado[i]['...nome']
			resultado[i]['tipo_logradouro'] = resultado[i]['....tipo_logadouro']
			resultado[i]['logradouro'] = resultado[i]['....logradouro']
			resultado[i]['num'] = resultado[i]['....numero']
			resultado[i]['bairro'] = resultado[i]['....bairro']
			resultado[i]['cidade'] = resultado[i]['....cidade']
			resultado[i]['uf'] = resultado[i]['....uf']
			resultado[i]['cep'] = resultado[i]['....cep']

			del resultado[i]['capacidade']
			del resultado[i]['.numero']
			del resultado[i]['.andar']
			del resultado[i]['..numero']
			del resultado[i]['...codigo']
			del resultado[i]['...nome']
			del resultado[i]['....tipo_logadouro']
			del resultado[i]['....logradouro']
			del resultado[i]['....numero']
			del resultado[i]['....bairro']
			del resultado[i]['....cidade']
			del resultado[i]['....uf']
			del resultado[i]['....cep']

		return resultado


class CriarCelas(Resource):
	def post(self):
		conn = Connection()

		try:
			codigo_unidade = str(request.json['codigo_unidade'])
			numero_pavilhao = str(request.json['fk_numero_pavilhao'])
			numero_bloco = str(request.json['fk_numero_bloco'])
		except:
			codigo_unidade = "null"
			numero_pavilhao = "null"
			numero_bloco = "null"
	
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

		try:
			codigo_unidade = str(request.json['codigo_unidade'])
			numero_pavilhao = str(request.json['fk_numero_pavilhao'])
			numero_bloco = str(request.json['fk_numero_bloco'])
		except:
			codigo_unidade = "null"
			numero_pavilhao = "null"
			numero_bloco = "null"
			
		codigo_cela = str(request.json['codigo'])

		capacidade = str(request.json['quantidade_max'])
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

		codigo_unidade = str(request.json['codigo_unidade'])
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

class ListarCelasPrisioneiros(Resource):
	def get(self):
		conn = Connection()

		codigo_unidade = str(request.args['fk_codigo_unidade'])
		numero_pavilhao = str(request.args['fk_numero_pavilhao'])
		numero_bloco = str(request.args['fk_numero_bloco'])
		codigo_cela = str(request.args['codigo'])

		command = (
			"select " + Util.formatQuery("p", "prisioneiro") +
			" from prisioneiros p" +
			" where p.cela =" +
			" (select ref(c) from celas c where c.codigo = " + codigo_cela
			 + ")"
		)

		prisioneiros = conn.query(command)

		if (prisioneiros['success'] == False):
			return prisioneiros

		resultado = []
		for data in prisioneiros['data']:
			resultado.append(Util.formatResponse(data, prisioneiros['columns'], []))

		return resultado

