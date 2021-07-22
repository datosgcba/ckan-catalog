from ckanapi import RemoteCKAN
import requests
from datetime import date, datetime

import json
import os,sys,inspect

import json
import os,sys,inspect

# Import organizaciones from common
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
data_lib_dir = os.path.join(parent_dir, "data_lib/")
migracion_dir = os.path.join(parent_dir, "migrar-portal/")
sys.path.insert(0,current_dir) 
sys.path.insert(0,migracion_dir) 
import organizaciones as util_org
import datasets as util_datasets
import usuarios as util_usuarios
import recursos as util_recursos

def MigrarRecursos(portal_origen, portal_destino):
	'''
	Recorre los organizaciones de portal_destino grabando para cada dataset 
	los recursos que ese dataset tiene en portal_origen
	'''
	# Primero reviso las organizaciones que se migraron y recorriendo los datasets
	# de cada una se migran todos los recursos de cada uno
	orgs = util_org.GetListaOrganizaciones(portal_destino)
	for organizacion in orgs:
		datasets_id = util_datasets.GetListaDatasetsOrganizacion(portal_destino, organizacion)
		for id in datasets_id:
			# Si el dataset en portal_destino tiene recursos lo ignoro
			# es un fix porque la migracion se corta por timeout al migrar muchos dataset
			dataset_destino = util_datasets.DetallarDataset(portal_destino, id)
			if(util_datasets.DatasetConRecurso(dataset_destino)):
				continue
			# Si el dataset no tiene recursos se los inserta
			print('Insertando recursos de ', id)
			dataset = util_datasets.DetallarDataset(portal_origen, id)
			for recurso in dataset['resources']:
				loops = 1
				respuesta = 'pending'
				print(respuesta, ' ', recurso['name'], ' loop ', loops)
				respuesta = util_recursos.CrearRecurso(portal_destino, recurso)
				print('respuesta al subir ', recurso['name'], ' es ', respuesta)
				while respuesta == 'pending':
					print('respuesta en loop ', loop, 'al subir recurso ', respuesta['name'])
					loop = loop + 1
			print(id, ' ------ \n')

def MigrarDatasets(portal_origen, portal_destino):
	'''
	Migrar Datasetsçç
	'''
	# primero obtengo las organizaciones que se migraron al portal_destino
	for i in util_org.GetListaOrganizaciones(portal_destino):
		# segundo obtengo desde portal_origen todos los dataset que pertenecen a cada organizacion
		datasets = util_datasets.GetDatasetsOrganizacion(portal_origen, i)
		#  después inserto en cada organizacion los datasets que le corresponden del 
		# portal_origen al portal_destino
		for dataset_a_importar in datasets:
			util_datasets.CrearDataset(portal_destino, dataset_a_importar)
			print('Importado dataset ', dataset_a_importar['name'])

def MigrarOrganizaciones(portal_origen, portal_destino):
	'''
	Migrar Organizaciones
	''' 
	migrarOrga = util_org.DetallarOrganizaciones(portal_origen)
	for i in migrarOrga:
		util_org.CrearOrganizaciones(portal_destino, i)
	# Actualizar los atributos de las organizaciones para acomodar estructura 
	# de Organizaciones, no se puede ordenar en la consuta porque 
	# no hay atributo para filtrarlo para todos los niveles de parentesco
	for i in migrarOrga:
		util_org.CrearOrganizaciones(portal_destino, i)
	# Reviso cuantas organizaciones se migraron
	print('Se importaron ', util_org.ContartOrganizaciones(portal_destino), ' Organizaciones')

def ListarRecursos(portal_destino):
	'''
	Recorre los organizaciones de portal_destino grabando para cada dataset 
	los recursos que ese dataset tiene en portal_origen
	'''
	# Primero reviso las organizaciones que se migraron y recorriendo los datasets
	# de cada una se migran todos los recursos de cada uno
	orgs = util_org.GetListaOrganizaciones(portal_destino)
	for organizacion in orgs:
		datasets_id = util_datasets.GetListaDatasetsOrganizacion(portal_destino, organizacion)
		for id in datasets_id:
			# Si el dataset en portal_destino tiene recursos lo ignoro
			# es un fix porque la migracion se corta por timeout al migrar muchos dataset
			dataset_destino = util_datasets.DetallarDataset(portal_destino, id)
			if(util_datasets.DatasetConRecurso(dataset_destino)):
				respuesta = util_datasets.GetDatasets(portal_destino, id)
				print(respuesta)

def ActualizarRecursosFiltro(portal_origen, portal_destino, filtro):
	'''
	Recorre los organizaciones de portal_destino y si esta dentro del 
	filtro de datasets se graba en portal_destino
	'''
	# Primero reviso las organizaciones que se migraron y recorriendo los datasets
	# de cada una se migran todos los recursos de cada uno
	orgs = util_org.GetListaOrganizaciones(portal_destino)
	
	for organizacion in orgs:
		datasets_id = util_datasets.GetListaDatasetsOrganizacion(portal_destino, organizacion)
		for id in datasets_id:
			
			# Si el id no esta en el filtro se ignora
			# dataset_destino = util_datasets.DetallarDataset(portal_destino, id)
			if(id not in filtro):
				#print('Ignorando id: ',id)
				continue
			# Si el dataset esta en el filtro se inserta
			print('Borrando recursos de ', id)
			util_datasets.BorrarRecursosDataset(portal_destino, id)
			print('Insertando recursos de ', id)
			dataset = util_datasets.DetallarDataset(portal_origen, id)
			for recurso in dataset['resources']:
				loops = 1
				respuesta = 'pending'
				print(respuesta, ' ', recurso['name'], ' loop ', loops)
				respuesta = util_recursos.CrearRecurso(portal_destino, recurso)
				print('respuesta al subir ', recurso['name'], ' es ', respuesta)
				while respuesta == 'pending':
					print('respuesta en loop ', loop, 'al subir recurso ', respuesta['name'])
					loop = loop + 1
			print(id, ' ------ \n')