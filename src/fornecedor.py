from flask import Flask, request
from flask_restful import Resource, Api

import sys
sys.path.insert(0, '..')
from Connection import Connection
from util import Util

app = Flask(__name__)
api = Api(app)


class ListarFornecedores(Resource):
    def get(self):
        conn = Connection()
        command = ("select " + Util.formatQuery('f', 'fornecedor') +
                   " from fornecedores f")

        fornecedores = conn.query(command)

        if (fornecedores['success'] == False):
            return fornecedores

        resultado = []
        for data in fornecedores['data']:
            resultado.append(Util.formatResponse(data, fornecedores['columns'], []))
        return resultado

class BuscarFornecedores(Resource):
    def get(self):
        conn = Connection()

        cnpj = str(request.args['cnpj'])

        command = ("select " + Util.formatQuery('f', 'fornecedor') +
                   " from fornecedores f" +
                   " where "+
                   " f.cnpj = " + cnpj)

        fornecedores = conn.query(command)

        if (fornecedores['success'] == False):
            return fornecedores

        resultado = []
        for data in fornecedores['data']:
            resultado.append(Util.formatResponse(data, fornecedores['columns'], []))

        return resultado

class CriarFornecedor(Resource):
    def post(self):
        conn = Connection()

        cnpj = str(request.json['cnpj'])
        nome_empresa = Util.formatString(request.json['nome_empresa'])

        itens = request.json['itens']

        itens_string = "Item_NT("

        for item in itens:
            itens_string = itens_string + Util.formatString(item) + ", "
        itens_string = itens_string[:-2]
        itens_string = itens_string + ")"

        command = (
                "insert into fornecedores values (" +
                cnpj + ", " +
                nome_empresa + ", " +
                itens_string+
                ")"
        )

        return conn.update(command)

class AlterarFornecedores(Resource):
    def post(self):
        conn = Connection()

        cnpj = str(request.json['cnpj'])

        nome_empresa = Util.formatString(request.json['nome_empresa'])
        itens = request.json['itens']

        if (len(itens) > 0):
            itens_string = "Item_NT("
            for item in itens:
                itens_string = itens_string + Util.formatString(item) + ", "
            itens_string = itens_string[:-2]
            itens_string = itens_string + ")"

        command = (
                "update fornecedores set " +
                "nome_empresa = " + nome_empresa
        )

        if (len(itens_string) > 0):
            command = (command + ", " +
                       "itens = " + itens_string)

        command += " where cnpj= "+cnpj
        return conn.update(command)

class RemoverFornecedores(Resource):
    def post(self):
        conn = Connection()

        cnpj = str(request.json['cnpj'])

        command = (
            "delete from fornecedores f where" +
            " f.cnpj = " + cnpj
        )
        return conn.update(command)