from ckanapi import RemoteCKAN
import requests

import json

def GetUsuarios(portal_origen, user_call_settings):
	'''
	Devuelve un diccionario  del portal de origen con todos los usuarios
	user_call_settings dict:
    q (string) – filter the users returned to those whose names contain a string (optional)
    email (string) – filter the users returned to those whose email match a string (optional) (you must be a sysadmin to use this filter)
    order_by (string) – which field to sort the list by (optional, default: 'display_name'). Users can be sorted by 'id', 'name', 'fullname', 'display_name', 'created', 'about', 'sysadmin' or 'number_created_packages'.
    all_fields (bool) – return full user dictionaries instead of just names. (optional, default: True)
	'''
	usuarios = portal_origen.call_action('user_list', user_call_settings)
	return usuarios

def GetDetalleUsuario(portal_origen, id):
	'''
	Devuelve una lista con todos los atributos de un usario del portal de origen 
	user_call_settings dict:
    id (string) – the id or name of the user (optional)
    user_obj (user dictionary) – the user dictionary of the user (optional)
    include_datasets (bool) – Include a list of datasets the user has created. If it is the same user or a sysadmin requesting, it includes datasets that are draft or private. (optional, default:False, limit:50)
    include_num_followers (bool) – Include the number of followers the user has (optional, default:False)
    include_password_hash (bool) – Include the stored password hash (sysadmin only, optional, default:False)
    include_plugin_extras (bool) – Include the internal plugin extras object (sysadmin only, optional, default:False)
	'''
	user_call_settings = {'id':'64a6cc13-ee07-40c3-85df-3da32def144f','include_num_followers':'true', 'include_password_hash':'true', 'include_plugin_extras':'true'}
	usuario = portal_origen.call_action('user_show', user_call_settings)
	result = []
	for user in usuario:
		result.append(user)
	return result

def GetListaUsuarios(portal_origen):
	'''
	Devuelve una lista con la totalidad de los usuarios del portal
	'''
	org_call_settings = {'order_by':'name'}
	usuarios = GetUsuarios(portal_origen, org_call_settings)
	users = []
	for i in usuarios:
		users.append(i)
	return users

def ImprimirListaUsuarios(portal_origen):
	'''
	Devuelve un string para imprimir en pantalla con la totalidad de los usuarios del portal
	'''
	org_call_settings = {'order_by':'name'}
	usuarios = GetUsuarios(portal_origen, org_call_settings)
	users = ''
	for i in usuarios:
		users = users + str(i) + '\n\n'
	return users

def CrearUsuario(portal_destino, usuario):
	'''
	Crea un usuario si no existe
	'''
	portal_destino.call_action('user_create', usuario)