from ckanapi import RemoteCKAN
import requests

import json

def GetOrganizaciones(portal_origen, org_call_settings):
	'''
	Devuelve un diccionario  del portal de origen con todas las organizaciones
	org_call_settings dict:
	  order_by (string) – the field to sort the list by, must be 'name' or 'packages' (optional, default: 'name') Deprecated use sort.
    sort (string) – sorting of the search results. Optional. Default: “title asc” string of field name and sort-order. The allowed fields are ‘name’, ‘package_count’ and ‘title’
    limit (int) – the maximum number of organizations returned (optional) Default: 1000 when all_fields=false unless set in site’s configuration ckan.group_and_organization_list_max Default: 25 when all_fields=true unless set in site’s configuration ckan.group_and_organization_list_all_fields_max
    offset (int) – when limit is given, the offset to start returning organizations from
    organizations (list of strings) – a list of names of the groups to return, if given only groups whose names are in this list will be returned (optional)
    all_fields (bool) – return group dictionaries instead of just names. Only core fields are returned - get some more using the include_* options. Returning a list of packages is too expensive, so the packages property for each group is deprecated, but there is a count of the packages in the package_count property. (optional, default: False)
    include_dataset_count (bool) – if all_fields, include the full package_count (optional, default: True)
    include_extras (bool) – if all_fields, include the organization extra fields (optional, default: False)
    include_tags (bool) – if all_fields, include the organization tags (optional, default: False)
    include_groups (bool) – if all_fields, include the organizations the organizations are in (optional, default: False)
    include_users (bool) – if all_fields, include the organization users (optional, default: False).
	'''
	organizaciones = portal_origen.call_action('organization_list', org_call_settings)
	return organizaciones

def ImprimirListaOrganizaciones(portal_origen):
	'''
	Devuelve un string con el nombre de cada organizacion del portal en varias lineas
	'''
	org_call_settings = {'sort': 'name', 'all_fields': 'true', 'include_extras': 'true', 'include_groups': 'true'}
	
	organizaciones = GetOrganizaciones(portal_origen, org_call_settings)
	nombres = ''
	for i in organizaciones:
		nombres = nombres + i['display_name'] + '\n'
	return(nombres)

def GetSliceOrganizaciones(portal_origen, num):
	'''
	Devuelve una lista de tamaño num con las organizaciones del portal de origen
	'''
	org_call_settings = {'sort': 'name', 'all_fields': 'true', 'include_extras': 'true', 'include_groups': 'true'}
	
	organizaciones = GetOrganizaciones(portal_origen, org_call_settings)
	count = 0
	orgs = []
	for i in organizaciones:
		if(count == num):
			break
		orgs.append(i)
		count += 1
	return(orgs)

def GetListaOrganizaciones(portal_origen):
	'''
	Devuelve una lista con los nombres de cada organizacion
	del portal de origen
	'''
	org_call_settings = {'sort': 'name'}
	
	organizaciones = GetOrganizaciones(portal_origen, org_call_settings)
	orgs = []
	for i in organizaciones:
		orgs.append(i)
	return(orgs)

def ImprimirOrganizaciones(portal_origen):
	'''
	Devuelve un string con la totalidad de las organizaciones del portal 
	'''
	org_call_settings = {'sort': 'name'}
	
	organizaciones = GetOrganizaciones(portal_origen, org_call_settings)
	orgs = ''
	for i in organizaciones:
		orgs = orgs + str(i) + '\n\n'
	return(orgs)

def DetallarOrganizaciones(portal_origen):
	'''
	Deveulve una lista con diccionarios, estos tienen todos los atributos de cada orgaizacion del portal de origen
	'''
	org_call_settings = {'sort': 'name', 'all_fields': 'true', 'include_extras': 'true', 'include_groups': 'true', 'include_users': 'true'}
	
	organizaciones = GetOrganizaciones(portal_origen, org_call_settings)
	orgs = []
	for i in organizaciones:
		orgs.append(i)
	return(orgs)

def ContartOrganizaciones(portal_origen):
	'''
	Devuelve la cantidad de organizaciones del portal de origen
	'''
	org_call_settings = {'sort': 'name'}
	
	organizaciones = GetOrganizaciones(portal_origen, org_call_settings)
	count = 0
	for i in organizaciones:
		count += 1
	return(count)

def CrearOrganizaciones(portal_destino, organizacion_dict):
	'''
	Crea o actualiza una organizacion en portal_destino
	'''
	portal_destino.call_action('organization_create', organizacion_dict)

