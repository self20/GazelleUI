import database as database
import wat as wat
import settings as settings

import urllib2

def queue(id):
  database.update('insert into torrents(id, added, downloaded) values ("' + id + '", datetime("now"), 0)')

def download_all():
  torrents = database.row_fetch('select * from torrents where downloaded = 0')
  for t in torrents:
    download_torrent(t[0])

def download_torrent(torrent_id):
  download_link = wat.download_link(torrent_id)
  download_path = settings.get('torrent')[1]
  save_to = download_path + torrent_id + ".torrent"

  opener = urllib2.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0')]
  torrent = opener.open(download_link).read()

  output = open(save_to,'wb')
  output.write(torrent)
  output.close()

  print "Downloaded " + torrent_id + ".torrent"
  database.update('update torrents set downloaded = 1 where id = "' + torrent_id + '"')