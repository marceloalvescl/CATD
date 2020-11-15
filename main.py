from flask import Flask, render_template, jsonify
import json
app = Flask(__name__)

@app.route('/')
def dashBoard():
  lista = readFile()
  return render_template('index.html', result=lista)

def readFile():
  f = open('./static/requisicoes.txt', 'r')
  lista = []
  for line in f:
    lista.append(json.loads(line))
  return lista