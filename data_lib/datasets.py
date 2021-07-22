from ckanapi import RemoteCKAN
import requests

import json

def GetDatasets(portal_origen, dataset_call_settings):
	'''
	Devuelve todos los atributos del dataset dataset_id del portal de origen
	data_dict:
    id (string) – the id or name of the dataset
    use_default_schema (bool) – use default package schema instead of a custom schema defined with an IDatasetForm plugin (default: False)
    include_tracking (bool) – add tracking information to dataset and resources (default: False)
	'''
	print(dataset_call_settings)
	dataset = portal_origen.call_action('package_show', dataset_call_settings)
	return dataset

def GetDatasetsList(portal_origen, dataset_call_settings={}):
	'''
	Devuelve una lista con los nombres de los dataset del portal de origen
	data_dict:
    limit (int) – if given, the list of datasets will be broken into pages of at most limit datasets per page and only one page will be returned at a time (optional)
    offset (int) – when limit is given, the offset to start returning packages from
	'''
	dataset = portal_origen.call_action('package_list', dataset_call_settings)
	return dataset

def GetDatasetsListFull(portal_origen, dataset_call_settings={'limit':'1000'}):
	'''
	Devuelve una lista con los nombres de los dataset del 
	portal de origen y sus recursos
	data_dict:   
    limit (int) – if given, the list of datasets will be broken into pages of at most limit datasets per page and only one page will be returned at a time (optional)
    offset (int) – when limit is given, the offset to start returning packages from
    page (int) – when limit is given, which page to return, Deprecated: use offset
	'''
	print(dataset_call_settings)
	dataset = portal_origen.call_action('current_package_list_with_resources', dataset_call_settings)
	return dataset

def GetDatasetsOrganizacion(portal_origen, org):
	'''
	Devuelve una lista con todos los datasets que pertenecen a una organizacion del portal de origen
	user_call_settings dict:
    id (string) – the id or name of the dataset
    use_default_schema (bool) – use default package schema instead of a custom schema defined with an IDatasetForm plugin (default: False)
    include_tracking (bool) – add tracking information to dataset and resources (default: False)
	'''
	datasets = portal_origen.call_action('organization_show', {'id':org, 'include_datasets':True})
	result = datasets['packages']
	return result

def GetListaDatasetsOrganizacion(portal_origen, org):
	'''
	Devuelve una lista con los nombres de los datasets que pertenecen a una organizacion del portal 
	'''	
	datasets = GetDatasetsOrganizacion(portal_origen, org)
	result = []
	for i in datasets:
		result.append(i['name'])
	return(result)

def ImprimirListaDatasetsOrganizacion(portal_origen, org):
	'''
	Devuelve un string para imprimir en pantalla con los nombres de los datasets
	que pertenecen a una organizacion del portal 
	'''	
	datasets = GetDatasetsOrganizacion(portal_origen, org)
	result = ''
	for i in datasets:
		result = result + str(i['name']) + '\n\n'
	return(result)

def DetallarPackageDataset(portal_origen, dataset_id):
	'''
	Devuelve un diccionario con todos los atributos de un dataset
	'''	
	apicall = portal_origen.call_action('package_show', {'id':dataset_id,'include_datasets':True})
	return apicall

def DetallarDataset(portal_origen, dataset_id):
	'''
	Devuelve un diccionario que tienen los atributos del dataset dataset_id
	'''	
	dataset_call_settings = {'id': dataset_id}
	datasets = GetDatasets(portal_origen, dataset_call_settings)
	#print(datasets)
	# result = {}
	# for i in datasets:
	# 	if(i == 'id'):
	# 		print(i, ' -- ', datasets[i])
	# 	result.append(i)
	# return(resuelt)
	return(datasets)

def ImprimirDetallarDataset(portal_origen, dataset_id):
	'''
	Devuelve un string par imprimir en pantalla que tiene los atributos 
	del dataset dataset_id
	'''	
	datasets = DetallarDataset(portal_origen, dataset_id)
	#print(datasets)
	result = ''
	for i in datasets:
		result = result + i + ' -- ' + str(datasets[i]) + '\n'
	return(result)

def DatasetConRecurso(dataset):
	'''
	Devuelve True si tiene recursos y False si no los tiene
	'''
	if(len(dataset['resources'])):
		return True
	else:
		return False

def GetRecursosDataset(portal_origen, dataset_id):
	'''
	Devuelve un diccionario que tiene los recursos del dataset dataset_id
	'''	
	dataset_call_settings = {'id': dataset_id}
	dataset = GetDatasets(portal_origen, dataset_call_settings)
	return(dataset['resources'])

def ImprimirRecursosDataset(portal_origen, dataset_id):
	'''
	Devuelve un string para imprimir en pantalla que tiene una lista de los 
	recursos del dataset dataset_id
	'''	
	dataset_call_settings = {'id': dataset_id}
	dataset = GetDatasets(portal_origen, dataset_call_settings)
	result = ''
	for recurso in dataset['resources']:
		for atributo in recurso:
			# convierto el valor del atributo en string porque no siempre lo es
			result = result + atributo + ': ' + str(recurso[atributo]) + '\n'
		result = result + '----\n'

		# result = result + recurso['name'] + '\n'
	return(result)

def BorrarRecursosDataset(portal_destino, dataset_id):
	'''
	Borrar todos los recursos de un dataset (dataset_id)
	'''
	dataset_call_settings = {'id': dataset_id}
	dataset = GetDatasets(portal_destino, dataset_call_settings)
	# Borro los recursos reemplazando los recursos por una lista con un diccionario vacio
	dataset['resources'] = [{}]
	portal_destino.call_action('package_update', dataset)

def CrearDataset(portal_destino, dataset):
	'''
	Crea un dataset si no existe
	'''
	portal_destino.call_action('package_create', dataset)

def ActualizarDataset(portal_destino, dataset):
	'''
	Actualiza un dataset si no existe
	id (string) – the name or id of the dataset to update
	'''
	portal_destino.call_action('package_patch', dataset)
