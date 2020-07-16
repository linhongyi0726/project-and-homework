import urllib.request, urllib.parse, urllib.error
import json
import os
import argparse

def callback(blocknum, blocksize, totalsize):
  percent = 100.0*blocknum*blocksize/totalsize
  if percent > 100:
    percent = 100
  print('%.2f%%' % percent)


serviceurl = 'https://www.xeno-canto.org/api/2/recordings?'

parser = argparse.ArgumentParser()
parser.add_argument("--country", type = str, required=True)
parser.add_argument("--count", type = int, required=True)
args = parser.parse_args()

country = args.country
count = args.count

parms = dict()
cnt = 'cnt:' + country
parms['query'] = cnt
url_test = serviceurl + urllib.parse.urlencode(parms)
url_test = url_test.replace('%3A',':')
uh_test = urllib.request.urlopen(url_test)
data_test = uh_test.read().decode()
js_test = json.loads(data_test)
numpages = int(js_test['numPages'])

retrieve_count = 0
data_count = 0
for page in range(1, numpages + 1):
  if retrieve_count > count: break
  parms['page'] = page
  url = serviceurl + urllib.parse.urlencode(parms)
  url = url.replace('%3A',':')
  uh = urllib.request.urlopen(url)
  data = uh.read().decode()
  js = json.loads(data)
  recordings = js['recordings']

  for recording in recordings:
    if retrieve_count >= count: break
    data_count = data_count + 1
    print(data_count)
    id = recording['id']
    gen = recording['gen'].lower()
    sp = recording['sp'].lower()
    ssp = recording['ssp'].lower()
    file = recording['file']
    if ssp == '':
      folder = gen + '_' + sp
    else:
      folder = gen + '_' + sp + '_' + ssp
    for char in folder:
      if char in '\/:*?"<>|':
        folder = folder.replace(char,'').strip()

    path = 'G:\\我的雲端硬碟\\SideProject\\Database\\' + folder
    path_anno = path + '\\annotations'
    path_mp3 = path + '\\mp3'

    if not os.path.exists(path):
      os.makedirs(path_anno)
      os.makedirs(path_mp3)
      print('Create folder', folder)

    jsonfile_name = id + '.json'
    mp3file_url = 'https:' + file
    mp3file_name = id + '.mp3'

    if os.path.exists(path_anno + '\\' + jsonfile_name) and os.path.exists(path_mp3 +'\\' + mp3file_name):
      print('ID', id, 'already retrieved')
      continue

    with open(path_anno + '\\' + jsonfile_name, 'w') as jsonfile:
      json.dump(recording, jsonfile, indent = 4)
      print('Retrieve json', jsonfile_name)

    try:
      urllib.request.urlretrieve(mp3file_url, path_mp3 +'\\' + mp3file_name, callback)
      print('Retrieve mp3', mp3file_name)
      retrieve_count = retrieve_count + 1
    except:
      with open('G:\\我的雲端硬碟\\SideProject\\Database\\mp3fail.txt','a+') as mp3fail:
        mp3fail.seek(0)
        if not str(id) in mp3fail.read():
          mp3fail.write('Bird name: ' + folder + '\nID: ' + str(id) + '\n\n')
          retrieve_count = retrieve_count + 1
      print('Fail to retrieve mp3', mp3file_name)

print('=== Already retrieved', retrieve_count, 'data in', country, '===')
