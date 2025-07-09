import requests
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="API de Cotação de Moedas",
    description="Uma API para consultar cotações de moedas e criptomoedas em tempo real e histórico.",
    version="1.0.0"
)

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

@app.get("/cotacao/agora/{coin_id}")
def get_current_price(coin_id: str, vs_currency: str = "brl"):
    """
        Gets the current price of a cryptocurrency in a specific currency.
    """
    try:
        url = f"{COINGECKO_API_URL}/simple/price?ids={coin_id}&vs_currencies={vs_currency}"
        
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()

        if coin_id not in data or vs_currency not in data[coin_id]:
            raise HTTPException(status_code=404, detail="Criptomoeda ou moeda de conversão não encontrada.")
            
        price = data[coin_id][vs_currency]
        
        return {
            "coin_id": coin_id,
            "currency": vs_currency,
            "price": price
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Erro ao contatar a API externa: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno: {e}")

@app.get("/converter")
def convert_currency(de: str, para: str, valor: float):
    """
    Converts a value from one currency/cryptocurrency to another.
    """
    try:
        
        url = f"{COINGECKO_API_URL}/simple/price?ids={de}&vs_currencies={para}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if de not in data or para not in data[de]:
            raise HTTPException(status_code=404, detail="Uma das moedas não foi encontrada.")

        taxa_conversao = data[de][para]
        valor_convertido = valor * taxa_conversao

        return {
            "valor_original": valor,
            "moeda_origem": de,
            "moeda_destino": para,
            "taxa_conversao": taxa_conversao,
            "valor_convertido": valor_convertido
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Erro ao contatar a API externa: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno: {e}")