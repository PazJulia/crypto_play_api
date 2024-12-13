from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import quote
from urllib.parse import unquote

from schemas import MoedaBuscaSchema, MoedaInfoShema
from schemas.error import ErrorSchema
from model import Session, Moeda
from flask_cors import CORS
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import json

info = Info(title="CryptoPlay API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
moeda_tag = Tag(name="Moeda", description="Adição, visualização e remoção de moedas à base")


@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')


@app.get('/moeda', tags=[moeda_tag], responses={"200": {}, "404": ErrorSchema})
def get_moedas_moeda(query: MoedaBuscaSchema):
    encoded_query = quote(query.nome)  # Encode the query parameter
    url = f"https://api.coingecko.com/api/v3/search?query={encoded_query}"

    try:
        req = Request(url, headers={
            'accept': 'application/json',
            'User-Agent': 'CryptoPlay/1.0'
        })
        content = urlopen(req).read()
        data = json.loads(content.decode('utf-8'))
        coins = data.get("coins", [])
        return {"coins": coins}
    except HTTPError as e:
        return {"error": f"HTTPError {e.code}: {e.reason}"}, e.code
    except URLError as e:
        return {"error": f"URLError: {e.reason}"}, 500
    except Exception as e:
        return {"error": str(e)}, 500

@app.get('/moeda/info', tags=[moeda_tag], responses={"200": {}, "404": ErrorSchema})
def get_info(query: MoedaInfoShema):
    # Verifica se 'coin_gecko_id' está presente e decodifica o valor
    coin_gecko_id = query.coin_gecko_id
    if not coin_gecko_id:
        return {"error": "O parâmetro 'coin_gecko_id' é obrigatório."}, 400

    # Decodifica caso venha URL-encoded
    coin_gecko_id = unquote(coin_gecko_id)

    # Constrói a URL para a API externa
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_gecko_id}&vs_currencies=brl"

    try:
        req = Request(url, headers={
            'accept': 'application/json',
            'User-Agent': 'CryptoPlay/1.0'
        })
        content = urlopen(req).read()
        dict_data = json.loads(content)
        return dict_data

    except HTTPError as e:
        return {"error": f"HTTPError {e.code}: {e.reason}"}, e.code
    except URLError as e:
        return {"error": f"URLError: {e.reason}"}, 500
    except Exception as e:
        return {"error": str(e)}, 500

# @app.post('/moeda/comprar', tags=[moeda_tag], responses={"200": {}, "404": ErrorSchema})
# def post_moeda(query: MoedaBuscaSchema):

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000, use_reloader=False)
