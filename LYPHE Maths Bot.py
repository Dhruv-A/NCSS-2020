from flask import Flask, jsonify, request
import re
import requests
from time import sleep
import base64
import urllib

app = Flask(__name__)


def build_data_url(mimetype, raw_bytes):
  base64_bytes = base64.b64encode(raw_bytes)
  base64_str = base64_bytes.decode('ascii')
  return f"data:{mimetype};base64,{base64_str}"
@app.route('/')
def hello():
  return 'Hello World'

@app.route('/greeting', methods=['POST'])
def hi():
  message = {
    'author': 'LYPHE',
    'text': f'Hi ',
  }
  data = request.get_json()
  text = data.get('text')
  part = re.findall('(hi|hey)(.*)', text.lower())
  part = part[0][1].split(' ')[-1].title()
  message['text'] = message['text'] + part
  return jsonify(message)

@app.route('/maths', methods=['POST'])
def maths():
  message = {
    'author': 'LYPHE',
    'text': "The answer is "
  }
  data = request.get_json()
  text = data.get('text')
  isCan = False
  if 'can' in text.lower():
    isCan = True
  part = re.findall('[0-9]+.*[0-9]+', text)
  sols = []
  for item in part:
    sols.append(str(eval(item)))
  message['text'] = message['text'] + 'and'.join(sols) + '.'
  if isCan:
    message['text'] = 'Yes I can!<br>' + message['text']
  return jsonify(message)

@app.route('/derive', methods=['POST'])
def derive():
  data = request.get_json()
  text = data.get('text')
  if 'derive' in text or 'differentiate' in text or 'derivative' in text:
    message = {
      'author': 'LYPHE',
      'text': 'The answer '
    }
    #takes question
    data = request.get_json()
    text = data.get('text')
    isCan = False
    if 'can' in text.lower():
      isCan = True
    wkey = 'LA3424-GW7V4VQREX'
    
    part = re.search('(?:derivative of|derive|differentiate) (.*)',text).groups()[-1]
    #prints equation

    
    print(part)
    # converts the equation in part so that its safe to put in url
    part = urllib.parse.quote_plus(part)
    url1 = f'http://api.wolframalpha.com/v1/spoken?appid={wkey}&i=what+is+the+derivative+of+{part}%3f'
    url2 = f'http://api.wolframalpha.com/v1/simple?appid={wkey}&i=what+is+the+derivative+of+{part}%3F'
    response = requests.get(url1)
    response = response.text
    response = re.search('(is .*)', response).groups()[-1]
    pic = requests.get(url2, stream=True)
    mimetype = pic.headers['Content-Type']
    raw_bytes = pic.content
    data_url = build_data_url(mimetype, raw_bytes)
    image_html = f'<img src="{data_url}">'
    TEMP = "https://www5b.wolframalpha.com/Calculate/MSP/MSP651140gdii12hh30ggb000056dbie7348eb1g3c?MSPStoreType=image/gif&s=56"
    """
    message['text'] = message['text'] + response + '.' + f"<br><img style='display:block; width:200px;height:200px;' id='base64image' src='data:image/gif;base64,{base64.encodebytes(pic)}'>"
    """
    message['text'] = message['text'] + response + '.' + f"<br>{image_html}"
    # message['text'] = message['text'] + response + '.' + f"<br><img style='display:block; width:200px;height:200px;' id='base64image' src='data:image/jpeg;base64', {pic}>"
    if isCan:
      message['text'] = 'Yes I can!<br>' + message['text']

    return jsonify(message)
  else:
    message = {
    'author': 'LYPHE',
    'text': "The answer is "
  }
  isCan = False
  if 'can' in text.lower():
    isCan = True
  part = re.findall('[0-9]+.*[0-9]+', text)
  sols = []
  for item in part:
    sols.append(str(eval(item)))
  message['text'] = message['text'] + 'and'.join(sols) + '.'
  if isCan:
    message['text'] = 'Yes I can!<br>' + message['text']
  return jsonify(message)
    

@app.route('/bored', methods=['POST'])
def bored():
  message = {
    'author': 'Bored bot',
    'text': 'I\'m bored as well!'
  }
  data = request.get_json()
  text = data.get('text')
  return jsonify(message)
'''

@app.route('/wolfram', methods=['POST'])
def derive():
  message = {
    'author': 'LYPHE',
    'text': 'The answer '
  }
  data = request.get_json()
  text = data.get('text')
  wkey = 'LA3424-GW7V4VQREX'
  part = re.search('(?:derivative of|derive|differentiate) (.*)',text).groups()[-1]
  url1 = f'http://api.wolframalpha.com/v1/spoken?appid={wkey}&i=what+is+the+derivative+of+{part}%3f'
  url2 = f'http://api.wolframalpha.com/v1/simple?appid={wkey}&i=what+is+the+derivative+of+{part}%3F'
  response = requests.get(url1)
  response = response.text
  response = re.search('(is .*)', response).groups()[-1]
  pic = requests.get(url2, stream=True)
  mimetype = pic.headers['Content-Type']
  raw_bytes = pic.content
  data_url = build_data_url(mimetype, raw_bytes)
  image_html = f'<img src="{data_url}">'
  TEMP = "https://www5b.wolframalpha.com/Calculate/MSP/MSP651140gdii12hh30ggb000056dbie7348eb1g3c?MSPStoreType=image/gif&s=56"
  """
  message['text'] = message['text'] + response + '.' + f"<br><img style='display:block; width:200px;height:200px;' id='base64image' src='data:image/gif;base64,{base64.encodebytes(pic)}'>"
  """
  message['text'] = message['text'] + response + '.' + f"<br>{image_html}"
  # message['text'] = message['text'] + response + '.' + f"<br><img style='display:block; width:200px;height:200px;' id='base64image' src='data:image/jpeg;base64', {pic}>"

  print(message)
  return jsonify(message) 
'''

app.run('0.0.0.0')
