# Sample Python code for user authorization

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0"

# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  # Trusted testers can download this discovery document from the developers page
  # and it should be in the same directory with the code.
  return build(API_SERVICE_NAME, API_VERSION,
      http=credentials.authorize(httplib2.Http()))

args = argparser.parse_args()
service = get_authenticated_service(args)

### END BOILERPLATE CODE

# Sample python code for channels.list

def channels_list_by_username(service, **kwargs):
  results = service.channels().list(
    **kwargs
  ).execute()

  print('This channel\'s ID is %s. Its title is %s, and it has %s views.' %
       (results['items'][0]['id'],
        results['items'][0]['snippet']['title'],
        results['items'][0]['statistics']['viewCount']))

def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs


def print_results(results):
  print(results)


def channels_list_by_id(service, **kwargs):
  kwargs = remove_empty_kwargs(**kwargs) # See full sample for function
  results = service.channels().list(
    **kwargs
  ).execute()

  print_results(results)

def videos_list_by_id(service, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)
    results = service.videos().list(**kwargs).execute()
    print_results(results)


def search_list_by_keyword(service, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)
    results = service.search().list(**kwargs).execute()
    print_results(results)

#channels_list_by_id(service,
#    part='snippet,contentDetails,statistics',
#    id='UC_x5XG1OV2P6uZZ5FSM9Ttw')

#channels_list_by_username(service, part='snippet,contentDetails,statistics', forUsername='ThomasDollar1')

#channels_list_by_id(service,
#    part='snippet,contentDetails,statistics',
#    id='Z0DJ1UBmS1sEjDBr2OABAw')


def build_resource(properties):
  resource = {}
  for p in properties:
    # Given a key like "snippet.title", split into "snippet" and "title", where
    # "snippet" will be an object and "title" will be a property in that object.
    prop_array = p.split('.')
    ref = resource
    for pa in range(0, len(prop_array)):
      is_array = False
      key = prop_array[pa]
      # Convert a name like "snippet.tags[]" to snippet.tags, but handle
      # the value as an array.
      if key[-2:] == '[]':
        key = key[0:len(key)-2:]
        is_array = True
      if pa == (len(prop_array) - 1):
        # Leave properties without values out of inserted resource.
        if properties[p]:
          if is_array:
            ref[key] = properties[p].split(',')
          else:
            ref[key] = properties[p]
      elif key not in ref:
        # For example, the property is "snippet.title", but the resource does
        # not yet have a "snippet" object. Create the snippet object here.
        # Setting "ref = ref[key]" means that in the next time through the
        # "for pa in range ..." loop, we will be setting a property in the
        # resource's "snippet" object.
        ref[key] = {}
        ref = ref[key]
      else:
        # For example, the property is "snippet.description", and the resource
        # already has a "snippet" object.
        ref = ref[key]
  return resource

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs

### END BOILERPLATE CODE

# Sample python code for playlists.list

def playlist_items_list_by_playlist_id(service, **kwargs):
  kwargs = remove_empty_kwargs(**kwargs) # See full sample for function
  results = service.playlistItems().list(
    **kwargs
  ).execute()

  print_results(results)

  playlist_item_idx=0
  while playlist_item_idx < len(results['items']):
      print (results['items'][playlist_item_idx]['snippet']['title'])
      playlist_item_idx = playlist_item_idx + 1




def playlists_list_by_channel_id(service, **kwargs):
  kwargs = remove_empty_kwargs(**kwargs) # See full sample for function
  results = service.playlists().list(
    **kwargs
  ).execute()

  print_results(results)

  playlist_idx=0
  while playlist_idx < len(results['items']):
      playlist_items_list_by_playlist_id(service,
                                         part='snippet, contentDetails',
                                         maxResults=25,
                                         playlistId=results['items'][playlist_idx]['id'])
      playlist_idx = playlist_idx + 1

playlists_list_by_channel_id(service,
    part='snippet,contentDetails',
    channelId='UCZ0DJ1UBmS1sEjDBr2OABAw',
    maxResults=50)


# channels_list_by_id(service,
#     part='snippet,contentDetails,statistics',
#     id='UCZ0DJ1UBmS1sEjDBr2OABAw')

# videos_list_by_id(service, part='snippet, contentDetails, statistics',
#                   id='75-aN75C3Y0')


# search_list_by_keyword(service,
#                         part='snippet',
#                         maxResults=25,
#                         q='TBH.eSports',
#                         type=' ')



# playlist_items_list_by_playlist_id(service,
#     part='snippet,contentDetails',
#     maxResults=25,
#     playlistId='PL0qwFDY6TCnxnYiOVi5SK5XMinZRR9wIE')

