from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import quote, unquote
from schemas import MoedaBuscaSchema, MoedaInfoShema, MoedaSchema
from schemas.error import ErrorSchema
from model import Session, Moeda, Usuario
from flask_cors import CORS
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json

# Configuração inicial da API
info = Info(title="CryptoPlay API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Tags da API
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
moeda_tag = Tag(name="Moeda", description="Adição, visualização e remoção de moedas à base")
usuario_tag = Tag(name="Usuário", description="Visualização de dados referentes ao saldo e lista de moedas do usuário")

# Endpoint para redirecionar para a documentação OpenAPI
@app.get('/', tags=[home_tag])
def home():
    """
    Redireciona para a documentação OpenAPI.
    """
    return redirect('/openapi')

# Endpoint para obter informações do usuário
@app.get('/usuario', tags=[usuario_tag], responses={"200": {}, "404": ErrorSchema})
def get_user_info():
    """
    Retorna as informações do usuário, incluindo saldo e moedas associadas.
    """
    session = Session()
    try:
        usuario = obter_usuario(session)
        if not usuario:
            return {"error": "Usuário não encontrado."}, 404

        # Serializar as moedas associadas ao usuário
        moedas = [
            {"id": moeda.id, "nome": moeda.nome, "coin_gecko_id": moeda.coin_gecko_id, "cota": moeda.cota, "simbolo_url": moeda.simbolo_url}
            for moeda in usuario.moedas
        ]

        # Retornar dados do usuário com suas moedas
        return {
            "id": usuario.id,
            "saldo_disponivel": usuario.saldo_disponivel,
            "balanco_total": usuario.balanco_total,
            "moedas": moedas
        }
    finally:
        session.close()

# Endpoint para buscar moedas
@app.get('/moeda', tags=[moeda_tag], responses={"200": {}, "404": ErrorSchema})
def get_moedas(query: MoedaBuscaSchema):
    """
    Realiza uma busca por moedas no CoinGecko, baseado no nome fornecido.
    """
    encoded_query = quote(query.nome)
    url = f"https://api.coingecko.com/api/v3/search?query={encoded_query}"

    try:
        req = Request(url, headers={'accept': 'application/json', 'User-Agent': 'CryptoPlay/1.0'})
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

# Endpoint para obter informações detalhadas sobre uma moeda
@app.get('/moeda/info', tags=[moeda_tag], responses={"200": {}, "404": ErrorSchema})
def get_info(query: MoedaInfoShema):
    """
    Retorna o valor de uma moeda em BRL usando o CoinGecko API, com base no `coin_gecko_id` fornecido.
    """
    coin_gecko_id = query.coin_gecko_id
    if not coin_gecko_id:
        return {"error": "O parâmetro 'coin_gecko_id' é obrigatório."}, 400

    # Decodifica o ID, caso esteja URL-encoded
    coin_gecko_id = unquote(coin_gecko_id)

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_gecko_id}&vs_currencies=brl"
    try:
        req = Request(url, headers={'accept': 'application/json', 'User-Agent': 'CryptoPlay/1.0'})
        content = urlopen(req).read()
        dict_data = json.loads(content)
        return dict_data
    except HTTPError as e:
        return {"error": f"HTTPError {e.code}: {e.reason}"}, e.code
    except URLError as e:
        return {"error": f"URLError: {e.reason}"}, 500
    except Exception as e:
        return {"error": str(e)}, 500

# Endpoint para processar a compra de uma moeda
@app.post('/moeda/comprar', tags=[moeda_tag], responses={"200": {}, "400": ErrorSchema, "404": ErrorSchema})
def post_moeda(form: MoedaSchema):
    """
    Processa a compra de uma moeda, verificando saldo, calculando a cota e atualizando o banco de dados.
    """
    session = Session()

    try:
        usuario = obter_usuario(session)
        if not usuario:
            return {"message": "Usuário não encontrado!"}, 404

        if not verificar_saldo_adequado(usuario, form.valor):
            return {"message": "Saldo insuficiente para realizar a compra!"}, 400

        cota_comprada = calcular_cota_comprada(form.valor, form.valor_moeda)
        processar_moeda(session, usuario, form, cota_comprada)
        atualizar_usuario(usuario, form.valor)

        session.commit()
        return {"message": "Moeda comprada com sucesso."}
    except Exception as e:
        session.rollback()
        return {"message": f"Erro ao processar a compra: {str(e)}"}, 500
    finally:
        session.close()

# Endpoint para excluir uma moeda
@app.delete('/moeda/del', tags=[moeda_tag], responses={"200": {}, "400": ErrorSchema, "404": ErrorSchema})
def del_moeda(query: MoedaInfoShema):
    """
    Exclui uma moeda do banco de dados e atualiza o saldo do usuário.
    """
    id = query.coin_gecko_id
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={id}&vs_currencies=brl"

    try:
        req = Request(url, headers={'accept': 'application/json', 'User-Agent': 'CryptoPlay/1.0'})
        content = urlopen(req).read()
        dict_data = json.loads(content)
        valor_brl = dict_data[id]['brl']

        session = Session()

        usuario = obter_usuario(session)
        if not usuario:
            return {"message": "Usuário não encontrado!"}, 404

        moeda = session.query(Moeda).filter(Moeda.coin_gecko_id == id).first()
        if not moeda:
            return {"message": "Moeda não encontrada!"}, 404

        cota_comprada_brl = moeda.cota * valor_brl
        usuario.saldo_disponivel += cota_comprada_brl
        usuario.balanco_total -= cota_comprada_brl

        session.delete(moeda)
        session.commit()

        return {"message": "Moeda removida e valores atualizados com sucesso."}
    except Exception as e:
        session.rollback()
        return {"message": f"Erro ao processar a remoção da moeda: {str(e)}"}, 500
    finally:
        session.close()

# Funções auxiliares

def obter_usuario(session):
    """
    Recupera o usuário atual do banco de dados.
    """
    try:
        return session.query(Usuario).first()
    except Exception as e:
        raise Exception(f"Erro ao obter o usuário: {str(e)}")

def verificar_saldo_adequado(usuario, valor_compra):
    """
    Verifica se o saldo disponível do usuário é suficiente para a compra.
    """
    return usuario.saldo_disponivel >= valor_compra

def calcular_cota_comprada(valor, valor_moeda):
    """
    Calcula a cota comprada (quantidade de moedas adquiridas).
    """
    return valor / valor_moeda

def processar_moeda(session, usuario, form, cota_comprada):
    """
    Processa a compra da moeda, atualizando ou criando um novo registro de moeda.
    """
    try:
        moeda = session.query(Moeda).filter(Moeda.coin_gecko_id == form.coin_gecko_id).first()
        if moeda:
            moeda.cota += cota_comprada
        else:
            nova_moeda = Moeda(
                nome=form.nome,
                coin_gecko_id=form.coin_gecko_id,
                cota=cota_comprada,
                simbolo_url=form.simbolo_url,
                usuario_id=usuario.id
            )
            session.add(nova_moeda)
    except Exception as e:
        raise Exception(f"Erro ao processar a moeda: {str(e)}")

def atualizar_usuario(usuario, valor_compra):
    """
    Atualiza o saldo e o balanço total do usuário após a compra.
    """
    try:
        usuario.saldo_disponivel -= valor_compra
        usuario.balanco_total += valor_compra
    except Exception as e:
        raise Exception(f"Erro ao atualizar o saldo do usuário: {str(e)}")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000, use_reloader=False)
