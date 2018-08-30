# coding: utf-8

import json
import urllib2
import sys

def obterNomeSeguidor(nomeSeguidor):
	dadosSeguidores = []
	API = 'https://api.github.com/users/{0}'
	
	linkAPI = API.format(nomeSeguidor)

	textoJson = verificarJSONExistente(linkAPI)
	textoJsonProcessado = json.loads(textoJson)

	return textoJsonProcessado['name']

def obterRepositorios(nomeSeguidor):
	nomes = []
	API = 'https://api.github.com/users/{0}/repos'
	
	url_processada = API.format(nomeSeguidor)

	textoJson = verificarJSONExistente(url_processada)
	textoJsonProcessado = json.loads(textoJson)

	
	for repositorio in textoJsonProcessado:
		nomes.append(repositorio['name'])

	return nomes
		 
def verificarJSONExistente(linkAPI):
	try:
		arquivo = open(linkAPI.replace('/', '-') + '.txt', 'r')
		textoJson = arquivo.read()
		return textoJson
	except Exception:
		try:
			textoJson = urllib2.urlopen(linkAPI).read()
			arq = open(linkAPI.replace('/', '-') + '.txt', 'w')
			arq.write(textoJson)
			arq.close()
			return textoJson
		except Exception as e:
			print '\n', e
			print 'Limite de requisições atingido'
			

API = 'https://api.github.com/users/{0}'
try:
	usuario = raw_input('\nNome do usuário GitHub: ')
	linkAPI = API.format(usuario)

	textoJson = verificarJSONExistente(linkAPI)

	textoJsonProcessado = json.loads(textoJson)

	urlUsuarios = textoJsonProcessado['followers_url']

	textoUrlProcessado = verificarJSONExistente(urlUsuarios)

	usuariosJson = json.loads(textoUrlProcessado)

	contadorSeguidores = textoJsonProcessado['followers']

	print '\nUsuário da Consulta: ', textoJsonProcessado['name'], '\n'

	print contadorSeguidores, ' seguidores: ', '\n'

	contUsuarios = 0
	contRepositorios = 0

	for usuario in usuariosJson:
		nome = usuario['login']
		print 'Seguidor' , contUsuarios+1, ': ', obterNomeSeguidor(nome), '\n'

		for repositorio in obterRepositorios(nome):	
			print '\t', 'Repositório', contRepositorios+1, ': ', repositorio
			contRepositorios += 1
		contRepositorios = 0
		print '\n'
		contUsuarios += 1
	print  contUsuarios, '/', contadorSeguidores, ' seguidores de ', textoJsonProcessado['name'], ' foram exibidos com sucesso!\n'
except Exception as e:
	print '\nPrograma fizalizado!\n'
