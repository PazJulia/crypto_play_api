# CriptoPlay API

CryptoPlay é uma aplicação web que permite simulação de compra e venda de criptomoedas, utilizando a API do CoinGecko para buscar informações atualizadas sobre os preços das moedas.

---

## Como executar

Será necessário ter todas as bibliotecas Python listadas no arquivo `requirements.txt` instaladas.

Após clonar o repositório, acesse o diretório raiz via terminal e execute os comandos abaixo.

> **Recomendação:** É fortemente indicado o uso de ambientes virtuais, como o [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

### No Linux/macOS:

1. Crie e ative o ambiente virtual:

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

2. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

3. Para executar a API, use o comando:

    ```bash
    flask run --host 0.0.0.0 --port 5000
    ```

4. Em modo de desenvolvimento, é recomendado usar o parâmetro `--reload` para reiniciar automaticamente o servidor a cada alteração no código:

    ```bash
    flask run --host 0.0.0.0 --port 5000 --reload
    ```

5. Abra [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

### No Windows:

1. Crie e ative o ambiente virtual:

    ```powershell
    python -m venv env
    .\env\Scripts\Activate.ps1
    ```

2. Instale as dependências:

    ```powershell
    pip install -r requirements.txt
    pip install -U flask-openapi3[swagger]
    ```

3. Para executar a API, use o comando:

    ```powershell
    flask run --host 0.0.0.0 --port 5000
    ```

4. Em modo de desenvolvimento, utilize o parâmetro `--reload`:

    ```powershell
    flask run --host 0.0.0.0 --port 5000 --reload
    ```

5. Acesse [http://localhost:5000/#/](http://localhost:5000/#/) para verificar o status da API.

---

## API CoinGecko

A CriptoPlay API utiliza a API pública do [CoinGecko](https://www.coingecko.com/), que fornece informações sobre preços de criptomoedas em tempo real, dados históricos, e muito mais.

A integração com a API CoinGecko é usada para obter informações detalhadas sobre as criptomoedas, como o preço atual de uma moeda em BRL (Real Brasileiro) e dados relacionados a ela. A API CoinGecko não requer uma chave de API e oferece uma maneira fácil de acessar dados confiáveis de criptomoedas.

---

### Notas

- **Flask:** O servidor web usado para esta API.
- **Flask-OpenAPI3:** Usado para integrar a documentação Swagger à API.
- **Requisitos:** Certifique-se de que todas as bibliotecas estão instaladas corretamente antes de executar a API.
- **API CoinGecko:** Fornece informações sobre preços e dados de criptomoedas, integrada para permitir o acesso a dados atualizados sobre as moedas que os usuários estão comprando ou vendendo.

---
