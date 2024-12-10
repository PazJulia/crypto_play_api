from pydantic import BaseModel
from typing import Optional, List
from model.moeda import Moeda

class MoedaSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    nome: str = "Bitcoin"

class MoedaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    nome: str = "BTC"

class MoedaInfoShema(BaseModel):
    """ Define a estrutura de busca de moeda pelo id do coinGecko
    """
    coin_gecko_id: str = "bitcoin"

# class ListagemProdutosSchema(BaseModel):
#     """ Define como uma listagem de produtos será retornada.
#     """
#     produtos:List[ProdutoSchema]
#
#
# def apresenta_produtos(produtos: List[Produto]):
#     """ Retorna uma representação do produto seguindo o schema definido em
#         ProdutoViewSchema.
#     """
#     result = []
#     for produto in produtos:
#         result.append({
#             "nome": produto.nome,
#             "quantidade": produto.quantidade,
#             "valor": produto.valor,
#         })
#
#     return {"produtos": result}
#
#
# class ProdutoViewSchema(BaseModel):
#     """ Define como um produto será retornado: produto + comentários.
#     """
#     id: int = 1
#     nome: str = "Banana Prata"
#     quantidade: Optional[int] = 12
#     valor: float = 12.50
#     total_cometarios: int = 1
#     comentarios:List[ComentarioSchema]
#
#
# class ProdutoDelSchema(BaseModel):
#     """ Define como deve ser a estrutura do dado retornado após uma requisição
#         de remoção.
#     """
#     mesage: str
#     nome: str
#
# def apresenta_produto(produto: Produto):
#     """ Retorna uma representação do produto seguindo o schema definido em
#         ProdutoViewSchema.
#     """
#     return {
#         "id": produto.id,
#         "nome": produto.nome,
#         "quantidade": produto.quantidade,
#         "valor": produto.valor,
#         "total_cometarios": len(produto.comentarios),
#         "comentarios": [{"texto": c.texto} for c in produto.comentarios]
#     }
