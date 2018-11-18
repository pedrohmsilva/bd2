import datetime

class Util:
	@staticmethod
	def formatQuery(index, entidade):
		entidades = {
			'up': ['codigo', 'nome'],
			'endereco': ['tipo_logadouro', 'logradouro', 'numero', 'bairro', 'cidade', 'uf', 'cep'],
			'pavilhao': ['numero', 'funcao'],
			'bloco': ['numero', 'andar'],
			'cela': ['codigo', 'capacidade', 'tipo'],
			'servidor': ['cpf', 'rg', 'nome', 'data_nascimento', 'cargo', 'salario']
		}

		string = ''

		for att in entidades[entidade]:
			string = string + index + '.' + att + ', '

		string = string[:-2]
		return string

	@staticmethod
	def formatResponse(valores, titulos, remove):
		resultado = {}

		for i in range(len(valores)):
			titulos[i] = titulos[i].lower()
			for r in remove:
				titulos[i] = titulos[i].replace(r, "")
			
			if isinstance(valores[i], datetime.datetime):
				resultado[titulos[i].lower()] = valores[i].__str__()
			else:
				resultado[titulos[i].lower()] = valores[i]

		return resultado

	@staticmethod
	def formatString(valor):
		return "'" + valor + "'"