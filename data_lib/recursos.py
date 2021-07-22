from ckanapi import RemoteCKAN
import requests

import json

def GetRecurso(portal_origen, dataset_call_settings):
	'''
	
	'''
	# dataset = portal_origen.call_action('package_show', dataset_call_settings)
	# return dataset

def GetListaRecurso(portal_origen, org):
	'''
	Devuelve una lista con los nombres de los datasets que pertenecen a una organizacion del portal 
	'''	
	# datasets = GetDatasetsOrganizacion(portal_origen, org)
	# result = []
	# for i in datasets:
	# 	result.append(i['name'])
	# return(result)

def ImprimirListaRecurso(portal_origen, org):
	'''
	Devuelve un string para imprimir en pantalla con los nombres de los datasets
	que pertenecen a una organizacion del portal 
	'''	
	# datasets = GetDatasetsOrganizacion(portal_origen, org)
	# result = ''
	# for i in datasets:
	# 	result = result + str(i['name']) + '\n\n'
	# return(result)

def DetallarRecurso(portal_origen, dataset_id):
	'''
	Devuelve un diccionario que tienen los atributos del dataset dataset_id
	'''	
	apicall = portal_origen.call_action('package_show', {'id':dataset_id,'include_datasets':True})
	result = apicall['resources']
	return result

def ImprimirDetallarRecurso(portal_origen, dataset_id):
	'''
	Devuelve un string par imprimir en pantalla que tiene los atributos 
	del dataset dataset_id
	'''	
	# datasets = DetallarDataset(portal_origen, dataset_id)
	# #print(datasets)
	# result = ''
	# for i in datasets:
	# 	result = result + i + ' -- ' + str(datasets[i]) + '\n'
	# return(result)

def CrearRecurso(portal_destino, recurso_dict):
	'''
	Crea un Recurso si no existe
	recurso_dict:
		package_id (string) – id of package that the resource should be added to.
		url (string) – url of resource
		description (string) – (optional)
		format (string) – (optional)
		hash (string) – (optional)
		name (string) – (optional)
		resource_type (string) – (optional)
		mimetype (string) – (optional)
		mimetype_inner (string) – (optional)
		cache_url (string) – (optional)
		size (int) – (optional)
		created (iso date string) – (optional)
		last_modified (iso date string) – (optional)
		cache_last_updated (iso date string) – (optional)
		upload (FieldStorage (
	'''
	portal_destino.call_action('resource_create', recurso_dict)
	# print(recurso_dict)