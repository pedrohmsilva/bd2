from flask import request
from flask_restful import Resource

import sys
sys.path.insert(0, '..')
from Connection import Connection
from util import Util

class ListarPavilhoes(Resource):
    def get(self):
        conn = Connection()
        pavilhoes = conn.query("select " + Util.formatQuery('p', 'pavilhao') + ", " + Util.formatQuery('p.unidade_prisional', 'up') + ", " + Util.formatQuery('p.unidade_prisional.endereco', 'endereco') + " from pavilhoes p")

        if (pavilhoes['success'] == False):
            return pavilhoes

        resultado = []
        for data in pavilhoes['data']:
            resultado.append(Util.formatResponse(data, pavilhoes['columns'], ['unidade_prisional.','endereco.']))

        return {
            "success": True,
            "data": resultado
        }
      
class BuscarPavilhoes(Resource):
    def get(self):
        conn = Connection()
        numero = request.args['numero']
        unidade_prisional = request.args['fk_unidade_prisional']
        pavilhoes = conn.query("select " + Util.formatQuery('p', 'pavilhao') + ", " 
        + Util.formatQuery('p.unidade_prisional', 'up') + ", " + Util.formatQuery('p.unidade_prisional.endereco', 'endereco') 
        + " from pavilhoes p where p.numero = " + numero + "and p.unidade_prisional.codigo = " + unidade_prisional)

        if (pavilhoes['success'] == False):
            return pavilhoes

        resultado = []
        for i in range(len(pavilhoes['data'])):
            resultado.append(Util.formatResponse(pavilhoes['data'][i], pavilhoes['columns'], ['unidade_prisional','endereco']))
            resultado[i]['codigo_unidade'] = resultado[i]['.codigo']
            del resultado[i]['.codigo']
            resultado[i]['nome_unidade'] = resultado[i]['.nome']
            del resultado[i]['.nome']
            resultado[i]['tipo_logradouro'] = resultado[i]['..tipo_logadouro']
            del resultado[i]['..tipo_logadouro']
            resultado[i]['logradouro'] = resultado[i]['..logradouro']
            del resultado[i]['..logradouro']
            resultado[i]['num'] = resultado[i]['..numero']
            del resultado[i]['..numero']
            resultado[i]['bairro'] = resultado[i]['..bairro']
            del resultado[i]['..bairro']
            resultado[i]['cidade'] = resultado[i]['..cidade']
            del resultado[i]['..cidade']
            resultado[i]['uf'] = resultado[i]['..uf']
            del resultado[i]['..uf']
            resultado[i]['cep'] = resultado[i]['..cep']
            del resultado[i]['..cep']

        '''
        for r in resultado:
            r['codigo_unidade'] = r['.codigo']
            r['nome_unidade'] = r['.nome']
            r['tipo_logradouro'] = r['..tipo_logadouro']
            r['logradouro'] = r['..logradouro']
            r['num'] = r['..numero']
            r['bairro'] = r['..bairro']
            r['cidade'] = r['..cidade']
            r['uf'] = r['..uf']
            r['cep'] = r['..cep']
        '''

        return {
            "success": True,
            "data": resultado
        }