from flask import Flask, jsonify
from flask_pydantic_spec import FlaskPydanticSpec
import datetime

app = Flask(__name__)

spec = FlaskPydanticSpec('flask',
                         title='datetime_API - SENAI',
                         version='1.0.0')

spec.register(app)


@app.route('/verificar-data/<dia>-<mes>-<ano>')
def verificar_data(dia, mes, ano):
    """
    API para calcular a diferença de dias meses e ano de duas datas

    ## Endpoint:
    `GET /verificar-data/<dia>-<mes>-<ano>`

    ## Parâmetros:
    - `dia, mes, ano` (int): **Data no formato "DD-MM-YYYY"** (exemplo: "12-09-2007").
        - **Qualquer outro valor irá resultar em erro.**

    ## Resposta (JSON)
    ```json
    {
        "anos_diferenca": 18,
        "data_agora": "27/03/2025",
        "data_inserida": "12/09/2007",
        "dias_diferenca": 6406,
        "meses_diferenca": 210,
        "situacao": "passado"
    }
    ```

    ## Erros possíveis:
    - Se `dia, mes, ano` não estiver no formato correto, retorna erro **400 Bad Request.**
    """
    try:
        # declaração de variáveis
        data = datetime.datetime(day=int(dia), month=int(mes), year=int(ano))
        agora = datetime.datetime.now()
        dias_diferenca = 0
        meses_diferenca = 0
        anos_diferenca = 0

        # situação
        if data == agora:
            situacao = "presente"
        elif data < agora:
            situacao = "passado"
        else:
            situacao = "futuro"

        # diferença
        if situacao == "passado" or situacao == "futuro":
            dias_diferenca = int(abs(data - agora).days)
            meses_diferenca = abs(((data.year - agora.year) * 12) + data.month - agora.month)
            anos_diferenca = abs(data.year - agora.year)
            if meses_diferenca % 12 == 0 and data.day - agora.day > 0:
                anos_diferenca = anos_diferenca - 1

            return jsonify({'anos_diferenca': anos_diferenca,
                            'dias_diferenca': dias_diferenca,
                            'meses_diferenca': meses_diferenca,
                            'situacao': situacao,
                            'data_agora': agora.strftime('%d/%m/%Y'),
                            'data_inserida': data.strftime('%d/%m/%Y')})
    except ValueError:
        return jsonify({'erro': 'Formato inválido'})


if __name__ == '__main__':
    app.run(debug=True)
