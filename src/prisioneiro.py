from flask import Flask, request
from flask_restful import Resource, Api

import sys
sys.path.insert(0, '..')
from Connection import Connection
from util import Util

app = Flask(__name__)
api = Api(app)

class ListarPrisioneiros(Resource):
	def get(self):
		conn = Connection()
		command = ("select " + Util.formatQuery('p', 'prisioneiro') + ", " + 
			Util.formatQuery('c', 'cela') + 
			" from prisioneiros p, celas c" + 
			" where ref(c) = p.cela")
			
		prisioneiros = conn.query(command)

		if (prisioneiros['success'] == False):
			return prisioneiros

		resultado = []
		for data in prisioneiros['data']:
			resultado.append(Util.formatResponse(data, prisioneiros['columns'], []))

		for i in range(len(resultado)):
			resultado[i]['cela_codigo'] = resultado[i]['codigo']
			resultado[i]['cela_capacidade'] = resultado[i]['capacidade']
			resultado[i]['cela_tipo'] = resultado[i]['tipo']
			del resultado[i]['codigo']
			del resultado[i]['capacidade']
			del resultado[i]['tipo']

			resultado[i]['observacoes_medicas'] = self.getObservacoesMedicas(resultado[i]['cpf'])
			resultado[i]['familiares'] = self.getFamiliares(resultado[i]['cpf'])

		return resultado
	
	def getObservacoesMedicas(self, cpf):
		conn = Connection()
		cpf = str(cpf)

		command = ("select * from TABLE(select observacoes_medicas from prisioneiros where cpf = " + cpf + ")")
		resultado = conn.query(command)

		observacoes = []
		for obs in resultado['data']:
			observacoes.append(obs[0])
		
		return observacoes

	def getFamiliares(self, cpf):
		conn = Connection()
		cpf = str(cpf)

		command = (
			"select * from TABLE(" +
				"select familiares from prisioneiros where cpf = " + cpf + 
			")"
		)

		familiares = conn.query(command)

		resultado = []
		for data in familiares['data']:
			resultado.append(Util.formatResponse(data, familiares['columns'], []))
		
		return resultado


class BuscarPrisioneiros(Resource):
	def get(self):
		conn = Connection()

		cpf = str(request.args['cpf'])

		command = ("select " + Util.formatQuery('p', 'prisioneiro') + ", " + 
			Util.formatQuery('c', 'cela') + 
			" from prisioneiros p, celas c" + 
			" where ref(c) = p.cela and" +
			" p.cpf = " + cpf)
			
		prisioneiros = conn.query(command)

		if (prisioneiros['success'] == False):
			return prisioneiros

		resultado = []
		for data in prisioneiros['data']:
			resultado.append(Util.formatResponse(data, prisioneiros['columns'], []))

		for i in range(len(resultado)):
			resultado[i]['cela_codigo'] = resultado[i]['codigo']
			resultado[i]['cela_capacidade'] = resultado[i]['capacidade']
			resultado[i]['cela_tipo'] = resultado[i]['tipo']
			del resultado[i]['codigo']
			del resultado[i]['capacidade']
			del resultado[i]['tipo']

			resultado[i]['observacoes_medicas'] = self.getObservacoesMedicas(resultado[i]['cpf'])
			resultado[i]['familiares'] = self.getFamiliares(resultado[i]['cpf'])

		return resultado
	
	def getObservacoesMedicas(self, cpf):
		conn = Connection()
		cpf = str(cpf)

		command = ("select * from TABLE(select observacoes_medicas from prisioneiros where cpf = " + cpf + ")")
		resultado = conn.query(command)

		observacoes = []
		for obs in resultado['data']:
			observacoes.append(obs[0])
		
		return observacoes

	def getFamiliares(self, cpf):
		conn = Connection()
		cpf = str(cpf)

		command = (
			"select * from TABLE(" +
				"select familiares from prisioneiros where cpf = " + cpf + 
			")"
		)

		familiares = conn.query(command)

		resultado = []
		for data in familiares['data']:
			resultado.append(Util.formatResponse(data, familiares['columns'], []))
		
		return resultado


class CriarPrisioneiros(Resource):
	def post(self):
		conn = Connection()

		cpf = str(request.json['cpf'])
		rg = Util.formatString(request.json['rg'])
		nome = Util.formatString(request.json['nome'])
		data_nascimento = "to_date('" + request.json['data_nascimento'] + "', 'yyyy-mm-dd')"

		cela = str(request.json['fk_cela'])
		observacoes_medicas = request.json['observacoes_medicas']
		familiares = request.json['familiares']

		familiares_string = "Familiares_NT("
		for i in range(len(familiares)):
			familiares_string = (familiares_string +
				"Familiar_TY (" +
					str(request.json['familiares'][i]['cpf']) + ", " +
					Util.formatString(request.json['familiares'][i]['rg']) + ", " +
					Util.formatString(request.json['familiares'][i]['nome']) + ", " +
					"to_date('" + request.json['familiares'][i]['data_nascimento'] + "', 'yyyy-mm-dd'), " +
					Util.formatString(request.json['familiares'][i]['parentesco']) +
				"), "
			)
		familiares_string = familiares_string[:-2]
		familiares_string = familiares_string + ")"

		observacoes_string = "Observacoes_Medicas_NT("
		for observacao in observacoes_medicas:
			observacoes_string = observacoes_string + Util.formatString(observacao) + ", "
		observacoes_string = observacoes_string[:-2]
		observacoes_string = observacoes_string + ")"
		
		command = (
			"insert into prisioneiros values (" +
				"Prisioneiro_TY (" +
					cpf + ", " +
					rg + ", " +
					nome + ", " +
					data_nascimento + ", " +
					"(select ref(c) from celas c where c.codigo = " + cela + "), " +
					observacoes_string + ", " +
					familiares_string +
				")" +
			")"
        )

		return conn.update(command)

class AlterarPrisioneiros(Resource):
	def post(self):
		conn = Connection()

		cpf = str(request.json['cpf'])

		rg = Util.formatString(request.json['rg'])
		nome = Util.formatString(request.json['nome'])
		data_nascimento = "to_date('" + request.json['data_nascimento'] + "', 'yyyy-mm-dd')"
		cela = request.json['fk_cela']
		observacoes_medicas = request.json['observacoes_medicas']
		familiares = request.json['familiares']

		if (len(familiares) > 0):
			familiares_string = "Familiares_NT("
			for i in range(len(familiares)):
				familiares_string = (familiares_string +
					"Familiar_TY (" +
						str(request.json['familiares'][i]['cpf']) + ", " +
						Util.formatString(request.json['familiares'][i]['rg']) + ", " +
						Util.formatString(request.json['familiares'][i]['nome']) + ", " +
						"to_date('" + request.json['familiares'][i]['data_nascimento'] + "', 'yyyy-mm-dd'), " +
						Util.formatString(request.json['familiares'][i]['parentesco']) +
					"), "
				)
			familiares_string = familiares_string[:-2]
			familiares_string = familiares_string + ")"

		if (len(observacoes_medicas) > 0):
			observacoes_string = "Observacoes_Medicas_NT("
			for observacao in observacoes_medicas:
				observacoes_string = observacoes_string + Util.formatString(observacao) + ", "
			observacoes_string = observacoes_string[:-2]
			observacoes_string = observacoes_string + ")"
		
		command = (
			"update prisioneiros set " +
				"rg = " + rg + ", " +
				"nome = " + nome + ", " +
				"data_nascimento = " + data_nascimento + ", " +
				"cela = (select ref(c) from celas c where c.codigo = " + cela + ")"
        )

		if (len(observacoes_string) > 0):
			command = (command + ", " +
				"observacoes_medicas = " + observacoes_string)
		
		if (len(familiares_string) > 0):
			command = (command + ", " +
				"familiares = " + familiares_string)

		return conn.update(command)

class RemoverPrisioneiros(Resource):
	def post(self):
		conn = Connection()

		cpf = str(request.json['cpf'])

		command = (
			"delete from servidores s where" +
			" s.cpf = " + cpf
		)

		return conn.update(command)

