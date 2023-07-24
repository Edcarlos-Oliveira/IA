from flask import Flask, jsonify, request
from Projeto_Final import *

# Comentários:
positivos = list()
negativos = list()

# Substantivos
subs_positivos = list()
subs_negativos = list()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def resultado():
    analisador(positivos, negativos)
    if (request.method == 'GET'):
        bd = banco_dados()
        cp = positivos
        cn = negativos
        pos = subst_positivos(subs_positivos, positivos)
        neg = subst_negativos(subs_negativos, negativos)
        return(jsonify({'Banco de Dados': bd}, {'Comentarios Positivos': cp}, {'Comentarios Negativos': cn}, {'Subst. Positivos': pos}, {'Subst. Negativos': neg}))
                      
if __name__=='__main__':
    app.run(debug=True, port=5000)
        
