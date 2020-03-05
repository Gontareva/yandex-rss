import json
import pprint
import time
from urlparse import urlparse

import requests
from requests import HTTPError

CULTURE_SESSION = requests.Session()
CULTURE_SESSION.headers.update({ 'Accept-version': '1.2.0'})
#
# HOST_ADDRESS = 'https://www.culture.ru/'
# OAUTH_TOKEN = 'AgAAAAAUie-IAAUEetCzE9FrcEZTlaAC3cbJDXw'
#
# AUTH_HEADER = {
#     'Authorization': 'OAuth %s' % OAUTH_TOKEN
# }
#
# SESSION = requests.Session()
# SESSION.headers.update(AUTH_HEADER)
#
# API_VERSION = 'v4'
# API_BASE_URL = 'https://api.webmaster.yandex.net'
# API_URL = API_BASE_URL + '/' + API_VERSION
#
#
# def validate_api_response(response, required_key_name=None):
#     content_type = response.headers['Content-Type']
#     content = json.loads(response.text) if 'application/json' in content_type else None
#
#     if response.status_code == 200:
#         if required_key_name and required_key_name not in content:
#             raise HTTPError('Unexpected API response. Missing required key: %s' % required_key_name, response=response)
#     elif content and 'error_message' in content:
#         raise HTTPError('Error API response. Error message: %s' % content['error_message'], response=response)
#     else:
#         response.raise_for_status()
#
#     return content
#
#
# def url_to_host_id(url):
#     parsed_url = urlparse(url)
#
#     scheme = parsed_url.scheme
#     if not scheme:
#         raise ValueError('No protocol (https or http) in url')
#
#     if scheme != 'http' and scheme != 'https':
#         raise ValueError('Illegal protocol: %s' % scheme)
#
#     port = parsed_url.port
#     if not port:
#         port = 80 if scheme == 'http' else 443
#
#     hostname = parsed_url.hostname
#     hostname = hostname.encode('idna').rstrip('.').lower()
#
#     return scheme + ':' + hostname + ':' + str(port)
#
#
# def get_user_id():
#     r = SESSION.get(API_URL + '/user/')
#     c = validate_api_response(r, 'user_id')
#
#     return c['user_id']
#
#
# def get_user_host_ids(user_id):
#     path = '/user/{user_id}/hosts'.format(user_id=user_id)
#     r = SESSION.get(API_URL + path)
#     c = validate_api_response(r, 'hosts')
#
#     host_ids = [host_info['host_id'] for host_info in c['hosts']]
#
#     return host_ids
#
#
# def is_user_host_id(user_id, host_id):
#     host_ids = get_user_host_ids(user_id)
#
#     return host_id in host_ids
#
#
# def get_rss_upload_path(user_id, host_id):
#     path = '/user/{user_id}/hosts/{host_id}/turbo/uploadAddress/?mode={mode}'.format(
#         user_id=user_id, host_id=host_id, mode='PRODUCTION')
#
#     r = SESSION.get(API_URL + path)
#     c = validate_api_response(r, 'upload_address')
#
#     parsed_url = c['upload_address']
#
#     return parsed_url
#
#
# def upload_rss(upload_path, rss_data):
#     headers = {
#         'Content-Type': 'application/rss+xml'
#     }
#
#     r = SESSION.post(url=upload_path, data=rss_data, headers=headers)
#     c = validate_api_response(r, 'task_id')
#
#     return c['task_id']
#
#
# def get_task_info(user_id, host_id, task_id):
#     path = '/user/{user_id}/hosts/{host_id}/turbo/tasks/{task_id}'.format(
#         user_id=user_id, host_id=host_id, task_id=task_id)
#
#     r = SESSION.get(API_URL + path)
#     c = validate_api_response(r)
#
#     return c
#
#
# def retry_call_until(func, predicate, max_tries=50, initial_delay=60, backoff=2):
#     current_delay = initial_delay
#
#     ret_val = None
#     for n_try in xrange(0, max_tries + 1):
#         ret_val = func()
#         if predicate(ret_val):
#             break
#
#         print ('Will retry. Sleeping for %ds' % current_delay)
#         time.sleep(current_delay)
#         current_delay *= backoff
#
#     return ret_val

RSS_HOST = 'http://127.0.0.1:7400'
CULTURE_HOST = 'http://127.0.0.1:7050'

def get_rss_data(page):
    print page
    print '%s/rss/yandex?entityType=%s&limit=%d&page=%d&sort=_id'%(RSS_HOST, entity_type, limit, page+1)
    rss = CULTURE_SESSION.get('%s/rss/yandex?entityType=%s&limit=%d&page=%d&sort=_id'%(RSS_HOST, entity_type, limit, page+1))
    return rss.text.encode("utf-8")

# user_id = get_user_id()
# host_id = url_to_host_id(HOST_ADDRESS)
# upload_path = get_rss_upload_path(user_id, host_id)

limit = 500
entity_type = 'persons'
entities = CULTURE_SESSION.get('%s/api/%s?fields=title,updateDate,status&limit=100&statuses=published'%(CULTURE_HOST, entity_type))
entities_pages = int(json.loads(entities.text)['pagination']['total'] * 100.0 / limit + 0.99)
print entities_pages
# entities_pages = 2

# f = open('rss.xml', 'a')
# entities_pages = 0
# for part in range(entities_pages+1):
#     rss_string = get_rss_data(part)
#
#     if not rss_string.find('<rss') == -1:
#         f.write(rss_string)
#         print 'cool'
#
# f.close()

f = open('rss.xml', 'r')


for part in range(entities_pages+1):
    rss_string = get_rss_data(part)
#     rss_string = f.read()
#     print rss_string
#
#     task_id = upload_rss(upload_path, rss_string)
#     print(task_id)
#
#     print 'Waiting for the upload task to complete. This will take a while...'
#     task_info = retry_call_until(
#         func=lambda: get_task_info(user_id, host_id, task_id),
#         predicate=lambda task_info: task_info['load_status'] != 'PROCESSING')
#
#     print 'Task status: %s' % task_info['load_status']
#     task_info = get_task_info(user_id, host_id, task_id)
#     pp = pprint.PrettyPrinter(indent=4)
#     pp.pprint(task_info)

f.close()
