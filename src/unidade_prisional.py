from flask import Flask, request, jsonify
from flask_restful import Resource, Api

import sys
sys.path.insert(0, '..')
from Connection import Connection

app = Flask(__name__)
api = Api(app)

columns = ['tipo_logradouro', 'nome']

def formatar(index, entidade):
	entidades = {
		'up': ['codigo', 'nome'],
		'endereco': ['tipo_logadouro', 'logradouro', 'numero', 'bairro', 'cidade', 'uf', 'cep']
	}

	string = ''

	for att in entidades[entidade]:
		string = string + index + '.' + att + ', '

	string = string[:-2]
	return string

def colunas(retorno, entidades):
	dicionario = {
		'up': ['codigo', 'nome'],
		'endereco': ['tipo_logadouro', 'logradouro', 'numero', 'bairro', 'cidade', 'uf', 'cep']
	}

	resultado = {}

	for valor in range(len(retorno)):
		if (valor < len(dicionario[entidades[0]])):
			resultado[dicionario[entidades[0]][valor]] = retorno[valor]
		else:
			resultado[dicionario[entidades[1]][valor - len(entidades[1])]] = retorno[valor]

	return resultado


class Listar(Resource):

	def get(self):
		conn = Connection()
		unidades = conn.query("select " + formatar('up', 'up') + ", " + formatar('up.endereco', 'endereco') + " from unidades_prisionais up")
		if (unidades['success'] == False):
			return unidades

		resultado = []
		for unidade in unidades['data']:
			unidade = colunas(unidade, ['up', 'endereco'])
			resultado.append(unidade)

		unidades['data'] = resultado
		return unidades

class Buscar(Resource):

	def get(self, codigo):
		conn = Connection()
		unidade = conn.query("select * from " + table + " where codigo = " + codigo)
		return unidade