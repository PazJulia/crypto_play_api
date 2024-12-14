from pydantic import BaseModel

class MoedaSchema(BaseModel):
    """ Define como uma nova moeda a ser comprada deve ser representada
    """
    nome: str = "Bitcoin"
    simbolo_url: str = ""
    coin_gecko_id: str = "bitcoin"
    valor_moeda: float = 600.0
    valor: float = 10.0

class MoedaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da moeda.
    """
    nome: str = "BTC"

class MoedaInfoShema(BaseModel):
    """ Define a estrutura de busca de moeda pelo id do coinGecko
    """
    coin_gecko_id: str = "bitcoin"