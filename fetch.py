import json
from urllib.parse import urlencode
import urllib.request

apikey = "89948ce1"

parameter = {}

def json_decoder(response):
    decoder = json.JSONDecoder()
    return decoder.decode(response)

def make_query(t,plot='short'):
    parameter["t"] = t
    parameter["plot"] = plot
    query = urlencode(parameter)#encodes the paramter string.
    request_url = "http://www.omdbapi.com/?"+query+"&apikey="+apikey+"" #Receives JSON data from the url
    #print(request_url)
    return request_url
    
def request(request_url):
    result =  json_decoder(urllib.request.urlopen(request_url).read().decode('utf-8')) #decodes JSON data from request_url
    try:
        return result['Plot'] #returns the "Plot" from the JSON data if found.
    except:
        return ("Sorry! The movie or tv show does not exist in the database.")