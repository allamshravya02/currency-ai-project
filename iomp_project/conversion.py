import requests
from config import EXCHANGE_API_KEY, BASE_URL

def convert_currency(from_currency, to_currency, amount):
    url = f"{BASE_URL}/{EXCHANGE_API_KEY}/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()

    rate = data["conversion_rates"][to_currency]
    converted_amount = round(amount * rate, 2)

    return {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "rate": rate,
        "converted_amount": converted_amount
    }
