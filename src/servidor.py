from flask import Flask, request
from flask_restful import Resource, Api

import sys
sys.path.insert(0, '..')
from Connection import Connection
from util import Util

app = Flask(__name__)
api = Api(app)

class ListarServidores(Resource):
	def get(self):
		conn = Connection()
		command = ("select " + Util.formatQuery('s', 'servidor') + ", " + Util.formatQuery('s.unidade_prisional', 'up') + ", " +
			Util.formatQuery('s.unidade_prisional.endereco', 'endereco') +
			" from servidores s")

		servidores = conn.query(command)

		if (servidores['success'] == False):
			return servidores

		resultado = []
		for data in servidores['data']:
			resultado.append(Util.formatResponse(data, servidores['columns'], ['unidade_prisional', 'endereco']))

		return resultado

class BuscarServidores(Resource):
	def get(self):
		conn = Connection()

		cpf = str(request.args['cpf'])

		command = ("select " + Util.formatQuery('s', 'servidor') + ", " +
			Util.formatQuery('s.unidade_prisional', 'up') + ", " +
			Util.formatQuery('s.unidade_prisional.endereco', 'endereco') +
			" from servidores s where " +
				"s.cpf = " + cpf
		)

		servidor = conn.query(command)

		if (servidor['success'] == False):
			return servidor

		resultado = []
		for data in servidor['data']:
			resultado.append(Util.formatResponse(data, servidor['columns'], ['unidade_prisional', 'endereco']))

		for i in range(len(resultado)):
			resultado[i]['codigo_unidade'] = resultado[i]['.codigo']
			resultado[i]['nome_unidade'] = resultado[i]['.nome']
			resultado[i]['tipo_logradouro'] = resultado[i]['..tipo_logadouro']
			resultado[i]['logradouro'] = resultado[i]['..logradouro']
			resultado[i]['num'] = resultado[i]['..numero']
			resultado[i]['bairro'] = resultado[i]['..bairro']
			resultado[i]['cidade'] = resultado[i]['..cidade']
			resultado[i]['uf'] = resultado[i]['..uf']
			resultado[i]['cep'] = resultado[i]['..cep']

			del resultado[i]['.codigo']
			del resultado[i]['.nome']
			del resultado[i]['..tipo_logadouro']
			del resultado[i]['..logradouro']
			del resultado[i]['..numero']
			del resultado[i]['..bairro']
			del resultado[i]['..cidade']
			del resultado[i]['..uf']
			del resultado[i]['..cep']

		return resultado


class CriarServidores(Resource):
	def post(self):
		conn = Connection()

		cpf = str(request.json['cpf'])
		rg = Util.formatString(request.json['rg'])
		nome = Util.formatString(request.json['nome'])
		data_nascimento = "to_date('" + request.json['data_nascimento'] + "', 'yyyy-mm-dd')"

		codigo_unidade = str(request.json['fk_codigo_unidade'])

		cargo = Util.formatString(request.json['cargo'])
		salario = str(request.json['salario'])
		
		command = (
			"insert into servidores values (" +
				"Servidor_TY (" +
					cpf + ", " +
					rg + ", " +
					nome + ", " +
					data_nascimento + ", " +
					"(select ref(up) from unidades_prisionais up where up.codigo = " + codigo_unidade + "), " +
					cargo + ", " +
					salario +
				")" +
			")"
        )

		return conn.update(command)

class AlterarServidores(Resource):
	def post(self):
		conn = Connection()

		cpf = str(request.json['cpf'])

		rg = Util.formatString(request.json['rg'])
		nome = Util.formatString(request.json['nome'])
		data_nascimento = "to_date('" + request.json['data_nascimento'] + "', 'yyyy-mm-dd')"
		cargo = Util.formatString(request.json['cargo'])
		salario = str(request.json['salario'])

		command = (
			"update servidores s set " +
				"s.rg = " + rg + ", " +
				"s.nome = " + nome + ", " +
				"s.data_nascimento = " + data_nascimento + ", " +
				"s.cargo = " + cargo + ", " +
				"s.salario = " + salario +
			" where " +
				"s.cpf = " + cpf
		)

		return conn.update(command)

class RemoverServidores(Resource):
	def post(self):
		conn = Connection()

		cpf = str(request.json['cpf'])

		command = (
			"delete from servidores s where" +
			" s.cpf = " + cpf
		)

		return conn.update(command)

