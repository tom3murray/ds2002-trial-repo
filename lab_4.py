# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import requests
import pandas

def get_api_response(url, response_type, header_v, stock_string):
    '''Acquire an API response from a URL.
    url: required argument containing a string of the desired URL to get a response from.
    response_type: required string argument indicating what format to give the response in.
    header_v: required argument giving the header for website access.
    stock_string: required argument indicating the stock string for Yahoo Finance API.
    Returns the response as a json. If an error is raised during the API hit, it indicates the error.'''
    try:
        response = requests.request("GET",url,headers=header_v,params=stock_string)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as errh:
        return "An Http Error occurred: " + repr(errh)
    except requests.exceptions.ConnectionError as errc:
        return "An Error Connecting to the API occurred: " + repr(errc)
    except requests.exceptions.Timeout as errt:
        return "A Timeout Error occurred: " + repr(errt)
    except requests.exceptions.RequestException as err:
        return "An Unknown Error occurred: " + repr(err)


# Create variables for get_api_response() function.
stock = input('Gimme a ticker: ')

header_var = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

url_quote = 'https://query1.finance.yahoo.com/v7/finance/quote'

query_string = {'symbols': stock}

response_type = ['json', 'dataframe']

# Execute get_api_response() function.
stock_result = get_api_response(url_quote, response_type[0], header_var, query_string)

print(stock_result)

# Isolate the ticker and name from the response.
ticker = stock_result['quoteResponse']['result'][0]['symbol']
name = stock_result['quoteResponse']['result'][0]['longName']

# Create variables for get_api_response() function.
url2 = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/"

query_string = {"symbol": stock, "modules":"financialData"}

response_type = ['json', 'dataframe']

stock_result = get_api_response(url2, response_type[0], header_var, query_string)

print(stock_result)

# Isolate the cashOnHand, currentPrice, targetMeanPrice, and profitMargin from the response.
cashOnHand = stock_result['quoteSummary']['result'][0]['financialData']['totalCash']['fmt']

currentPrice = stock_result['quoteSummary']['result'][0]['financialData']['currentPrice']['fmt']

targetMeanPrice = stock_result['quoteSummary']['result'][0]['financialData']['targetMeanPrice']['fmt']

profitMargin = stock_result['quoteSummary']['result'][0]['financialData']['profitMargins']['fmt']

# Return the isolated variables in a dictionary.
stock_dictionary = {
    "ticker": ticker,
    "name": name,
    "cashOnHand": cashOnHand,
    "currentPrice": currentPrice,
    "targetMeanPrice": targetMeanPrice,
    "profitMargin": profitMargin
}

# Turn the dictionary into a json object.
json_object = json.dumps(stock_dictionary, indent=4)