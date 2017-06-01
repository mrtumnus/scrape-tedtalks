# File:		download_tedtalk.py
# Author:	E. Partridge
# Date:		8 August 2012
# Description:
#			This script parses the TED Talk audio feed and proceeds to
#			download all audio files into the same directory that
#			this script is located in.  Files are prepended with the publication
#			date for convenience.
#
# Note: 	This has only been tested on Windows 7 64-bit, with Python 2.7.2.5
# Note2: 	TED Talk audio files contain ID3v2.4 tags, which are not supported
# 		 	natively by Windows. I used foobar2000 to convert the tags to ID3v2.3,
#			which Windows does support. To do this, open the MP3 files in
#			foobar2000, right click and select Tagging > MP3 Tag Types... Check
#			"Override ID3v2 revision:" and select the ID3v2.3 radio button.
#			After that, I was able to view metadata in Windows Explorer and
#			Windows Media Player.
import urllib
import feedparser
import time

tedtalk_rss_url = 'http://feeds.feedburner.com/TEDTalks_audio'
tedtalk_feed = feedparser.parse(tedtalk_rss_url)

def GetFeedContent(entry):
	content_url = entry.enclosures[0].href
	file_name = content_url.split('/')[-1]
	file_date = time.strptime(entry.published[5:16], '%d %b %Y')
	date_str = '{:04}-{:02}-{:02}'.format(file_date.tm_year, file_date.tm_mon, file_date.tm_mday)
	file_name = date_str + ' ' + file_name
	try:
		with open(file_name) as f:
			print('File exists: ' + file_name)
	except IOError as e:
		print('Downloading: ' + file_name)
		urllib.urlretrieve(content_url, file_name)
	return

for entry in tedtalk_feed.entries:
	GetFeedContent(entry)