class Util:
	@staticmethod
	def formatQuery(index, entidade):
		entidades = {
			'up': ['codigo', 'nome'],
			'endereco': ['tipo_logadouro', 'logradouro', 'numero', 'bairro', 'cidade', 'uf', 'cep'],
			'pavilhao': ['numero', 'funcao'],
			'bloco': ['numero', 'andar'],
			'cela': ['codigo', 'capacidade', 'tipo']
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
			resultado[titulos[i].lower()] = valores[i]

		return resultado

	@staticmethod
	def formatString(valor):
		return "'" + valor + "'"