from flask import Flask, jsonify, request
import requests
import os
from coinSlugNames import coin_symbol_to_slug_map


app = Flask(__name__)
port = os.getenv('PORT', default=10000)


def get_active_coin_names():
    try:
        url = 'https://mudrex.com/api/coin-services/v1/coins/metadata'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            if isinstance(data, dict):
                # only add the symbol if coin.is_active is true
                symbol_list = [coin['symbol']
                               for coin in data['data'].values() if coin['is_active']]

                return symbol_list
            else:
                raise Exception("Unexpected response format")
        else:
            raise Exception(
                f"API request failed with status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred in get_active_coin_names: {e}")
        return []


def get_active_coin_slugs():
    active_coin_names = get_active_coin_names()
    symbol_to_slug = {coin['symbol']: coin['slug']
                      for coin in coin_symbol_to_slug_map}

    result = []
    for coin in active_coin_names:
        if coin in symbol_to_slug:
            result.append(symbol_to_slug[coin])
        else:
            result.append(coin)

    return result


@app.route('/get-active-coins-urls', methods=['GET'])
def get_active_coins_urls():
    active_coin_slugs = get_active_coin_slugs()
    return jsonify([f"https://mudrex.com/coins/{slug.lower()}" for slug in active_coin_slugs])


@app.route('/get-active-buy-urls', methods=['GET'])
def get_active_buy_urls():
    active_coin_slugs = get_active_coin_slugs()
    return jsonify([f"https://mudrex.com/buy-{slug.lower()}" for slug in active_coin_slugs])


@app.route('/get-active-converter-urls', methods=['GET'])
def get_active_converter_urls():
    currency = request.args.get('currency', 'inr').lower()

    if not currency.isalnum() or len(currency) > 10:
        return jsonify({'error': 'Invalid currency format. Use alphanumeric characters only, max 10 characters.'}), 400

    active_coin_slugs = get_active_coin_slugs()
    return jsonify([f"https://mudrex.com/converter/{slug.lower()}/{currency}" for slug in active_coin_slugs])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port, debug=False)
