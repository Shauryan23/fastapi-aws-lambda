import pickle
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from mangum import Mangum
import uvicorn
import math
import re
import requests
import numpy as np

def count_digits(word):
  return len(re.findall('[0-9]', word))

def count_alphabets(word):
  return len(re.findall('[A-z]', word))

def count_special_characters(input_string):
  special_characters = "!@#$%^&*()-_=+[]{}|;:',.<>/?"
  count = 0

  for char in input_string:
    if char not in special_characters and not char.isalnum():
      count += 1

  return count

def remove_special_characters(input_string):
  # Pattern to match any non-alphanumeric and non-space character
  pattern = r'[^a-zA-Z0-9\s]'  
  return re.sub(pattern, '', input_string)

def calculate_entropy(word):
  if len(word) == 0:
    return 0

  entropy = 0
  word_length = len(word)
  char_count = {}

  for char in word:
    if char in char_count:
      char_count[char] += 1
    else:
      char_count[char] = 1

  for char in char_count:
    probability = char_count[char] / word_length
    entropy += -probability * math.log2(probability)

  return entropy

def whois_request(domain):
  querystring = {
    "domainName":domain,
    "apiKey":"at_riRl0t87FR3oUPp9DH9EfewVqDOgD",
    "outputFormat":"JSON",
    "da":"0",
    "ipwhois":"1",
    "thinWhois":"0",
    "_parse":"0",
    "preferfresh":"1",
    "checkproxydata":"0",
    "ip":"1"
  }

  headers = {
    "X-RapidAPI-Key": "d2592fe48dmsh190428470dadf9cp1bf762jsnf40816e6115e",
    "X-RapidAPI-Host": "whoisapi-whois-v2-v1.p.rapidapi.com"
  }

  url = "https://whoisapi-whois-v2-v1.p.rapidapi.com/whoisserver/WhoisService"

  response = requests.get(url, headers=headers, params=querystring)
  
  response_data = response.json()

  if "ErrorMessage" in response_data:
    created_year = -1
    updated_year = -1
    expires_year = -1
    country_code = "-1"
    domain_age = -1

  if "WhoisRecord" in response_data:
    if "createdDate" in response_data["WhoisRecord"]:
      created_year = response_data["WhoisRecord"]["createdDate"][0:4]
    elif "registryData" in response_data["WhoisRecord"] and "createdDate" in response_data["WhoisRecord"]["registryData"]:
      created_year = response_data["WhoisRecord"]["registryData"]["createdDate"][0:4]
    else:
      created_year = -1

  if "WhoisRecord" in response_data:
    if "updatedDate" in response_data["WhoisRecord"]:
      updated_year = response_data["WhoisRecord"]["updatedDate"][0:4]
    elif "registryData" in response_data["WhoisRecord"] and "updatedDate" in response_data["WhoisRecord"]["registryData"]:
      updated_year = response_data["WhoisRecord"]["registryData"]["updatedDate"][0:4]
    else:
      updated_year = -1

  if "WhoisRecord" in response_data:
    if "expiresDate" in response_data["WhoisRecord"]:
      expires_year = response_data["WhoisRecord"]["expiresDate"][0:4]
    elif "registryData" in response_data["WhoisRecord"] and "expiresDate" in response_data["WhoisRecord"]["registryData"]:
      expires_year = response_data["WhoisRecord"]["registryData"]["expiresDate"][0:4]
    else:
      expires_year = -1

  if "WhoisRecord" in response_data:
    if ("registrant" in response_data["WhoisRecord"] and 
      "countryCode" in response_data["WhoisRecord"]["registrant"]):
      country_code = response_data["WhoisRecord"]["registrant"]["countryCode"]
    elif (
      "registryData" in response_data["WhoisRecord"] and
      "registrant" in response_data["WhoisRecord"]["registryData"] and
      "countryCode" in response_data["WhoisRecord"]["registryData"]["registrant"]):
      country_code = response_data["WhoisRecord"]["registryData"]["registrant"]["countryCode"]
    else:
      country_code = "-1"
      
  if "WhoisRecord" in response_data and "estimatedDomainAge" in response_data["WhoisRecord"]:
    domain_age = response_data["WhoisRecord"]["estimatedDomainAge"]
  else:
    domain_age = -1

  parsed_response = [country_code, domain_age, created_year, updated_year, expires_year]
  return parsed_response

def build_input(URL):
  # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
  domain = URL.split("/")[0]
  if(domain=="https:" or domain=="http:"):
    domain = URL.split("/")[2]
  url_length = len(URL)

  # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
  domain_entropy = calculate_entropy(domain)

  # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
  temp = URL.split("/")
  subdomain = temp[0].split(".")[-1]

  # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
  path_rest = "/".join(temp[1:])
  path_rest_length = len(path_rest)

  # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
  tld = domain.split(".")[-1]
  tld_length = len(tld)
  tld = tld.split(":")[0]

  # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
  num_spcs_chars = count_special_characters(path_rest)

  # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
  whois_response = whois_request(URL)

  # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
  with open("./data/words_in_url.txt", "r") as file:
    content = file.read()  
  all_words_list = content.split()

  words_list = re.split(r"[/,.,?,-,+,=,&,~,!,@,#,$,%,_,;]", URL)

  def count_words_in_list(words_list, all_words_list):
    count = 0
    for word in words_list:
      if word in all_words_list:
        count += 1
    return count

  word_count = count_words_in_list(words_list, all_words_list)

  # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
  with open("./data/tld_in_rest_path.txt", "r") as file:
    content = file.read()
  all_tlds_list = content.split()

  def tld_words_in_list(tlds_list, all_tlds_list):
      count = 0
      for word in tlds_list:
          # Additional condition to check word length
          if len(word) > 1 and len(word) < 10:
              if word in all_tlds_list:
                  count += 1
      return count

  if(path_rest_length >0 ):
    tlds_list = re.split(r"[/,.,?,-,+,=,&,~,!,@,#,$,%,_,;]", path_rest)
    tld_in_path_rest = tld_words_in_list(tlds_list, all_tlds_list)
  else:
    tld_in_path_rest = 0

  # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
  input = np.array([tld, whois_response[0], url_length, path_rest_length, num_spcs_chars, domain_entropy, whois_response[1], whois_response[2], whois_response[3], whois_response[4], word_count, tld_in_path_rest], dtype=object).reshape(1, 12)

  return input

# Load the saved Model
clf_path = "model/classifier.pkl"
with open("./model/classifier.pkl", "rb") as file:
    clf = pickle.load(file)

app = FastAPI()
handler = Mangum(app)

@app.get("/")
async def home():
    return {"Data": "Home Page"}

@app.post("/test")
async def test(link: str):
    link = link.strip()
    inp = build_input(link)
    prediction = clf.predict(inp)
    print(prediction)
    print(type(prediction))
    prediction = prediction.tolist()
    return {"PREDICTION": prediction}

@app.post("/predict")
async def predict(web_links: dict):
    return web_links

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)