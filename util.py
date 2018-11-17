class Util:
	def formatQuery(index, entidade):
		entidades = {
			'up': ['codigo', 'nome'],
			'endereco': ['tipo_logadouro', 'logradouro', 'numero', 'bairro', 'cidade', 'uf', 'cep']
		}

		string = ''

		for att in entidades[entidade]:
			string = string + index + '.' + att + ', '

		string = string[:-2]
		return string

	def formatResponse(valores, titulos, remove):
		resultado = {}

		for i in range(len(valores)):
			titulos[i] = titulos[i].lower()
			for r in remove:
				titulos[i] = titulos[i].replace(r, "")
			resultado[titulos[i].lower()] = valores[i]

		return resultado