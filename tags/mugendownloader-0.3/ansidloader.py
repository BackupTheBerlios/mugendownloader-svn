#!/usr/bin/env python
# -*- coding: utf-8 -*-
# main.py
# Copyright (C) WoodenJesus 2007 <woodenjesus666@gmail.com>
# 
# ansidloader.py is free software.
# 
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 2 of the License, or (at your option)
# any later version.
# 
# ansidloader.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with main.py.  If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.

__version__ = '0.0.1'
__name__="ansidloader"

from urllib2 import *
from urllib import *
from cookielib import *
from codecs import *

import os

def printer(obj):
	print  obj,

class AnsiDloader:

	def __init__(self):
		self.mainpage = 'http://animesub.info'
		self.links = []
		
		self.cookie = CookieJar()
		opener = build_opener(HTTPCookieProcessor(self.cookie))
		self.urlopen = opener.open
		pass
		

		
	def findsub (self, string, dir = '', output = printer, pageno = 0, Autor = '', od = ('', '', ''), do = ('', '', '')):
		#http://animesub.info/szukaj.php?pGdzie=1&szukane=%21&pBezSlow=&ID=&pAutor=Freeman&pUdostepnil=&pFormat=&pIleCd=&pOd1=01&pOd2=02&pOd3=2006&pDo1=12&pDo2=31&pDo3=2008&pSortuj=traf
		
		string = string.replace(' ', '+')
		string = string.decode ('utf-8')
		string = string.encode ('iso-8859-2')
		if len (dir) != 0:
			dir =  dir + '/' 

		done = False 
		self.links = []
		self.subtitles_number = 0
		
		while done != True:
			
			del self.links[:]
		
			output ( "\nSTRONA " + str('%10d'% pageno) + "\n\n")
			
			page = self.urlopen (self.mainpage + '/szukaj.php?pGdzie=1&szukane='+string+'&pSortuj=t_ang&od='+ str(pageno) + '&pAutor=' + Autor + '&pOd1=' + str(od[2]) +'&pOd2=' + str(od[1] + 1) + '&pOd3=' + str(od[0]) +'&pDo1=' + str(do[2]) + '&pDo2=' + str(do[1] +1 ) + '&pDo3=' +str(do[0]) + '&Sortuj=traf')
			print self.mainpage + '/szukaj.php?pGdzie=1&szukane='+string+'&pSortuj=t_ang&od='+ str(pageno) + '&pAutor=' + Autor + '&pOd1=' + str(od[2]) +'&pOd2=' + str(od[1] + 1) + '&pOd3=' + str(od[0]) +'&pDo1=' + str(do[2]) + '&pDo2=' + str(do[1] +1 ) + '&pDo3=' +str(do[0]) + '&Sortuj=traf'
			pageno = pageno + 1
			
			page = page.read()
			page = page.decode ('iso-8859-2')
			page = page.encode ('utf-8')
			
			#print page
			
			notfound = 'Nie znaleziono napis'
			
			if page.find (notfound) != -1:
				done = True
				output ('KONIEC\n')
			
			self.regex = re.compile ('<a href=\"osoba\.php\?id=\d+\">[~#@]([@\-łąęóżźćń"\(\)\s\w]+)</a>')
			self.author = self.regex.findall(page)
			#print self.author
			#print len (self.author)
			
			self.regex = re.compile ('name=\"id\" value=\"(\d+)\"')
			self.id = self.regex.findall(page)
			#print len (self.id)
			
			self.regex = re.compile ('<tr class=\"KNap\"><td align=\"left\">(.+)</td><td><a href=\"javascript:PK')
			self.name = self.regex.findall(page)
			#print len (self.name)
			
			self.regex = re.compile ('<input type=\"hidden\" name=\"sh\" value=\"(.+)\">')
			self.sh = self.regex.findall(page)
			#print len (self.sh)

			for i in range (0, len(self.id)):
				self.links.append ((self.id[i], self.name[i], self.author[i], self.sh[i]))
				
			#done = True 
			
			#self.download (range (0, len(run.links)))
			
			for i in range (0, len(self.links)):
				post = urlencode ( {'sh': str(self.links[i][3]), 'id': str(self.links[i][0]) } )
				self.file = self.urlopen (self.mainpage + '/sciagnij.php', post)
				
				checkregex = re.compile ('filename=(.+\.zip)')
				filecheck = checkregex.findall(str(self.file.info()))
				
				if len (filecheck) == 1:
					
					print self.links[i]
					checkregex_dir = re.compile ('\sep.+')
					dircheck = checkregex_dir.sub('', str(self.links[i][1]))
					dir_friendly = re.compile ('[\/\\:\*\?"<>\|\.]')
					dircheck = dir_friendly.sub('', dircheck)

					print filecheck
					print dir
					print dircheck
					#dircheck = page.decode ('iso-8859-2')
					#page = page.encode ('utf-8')
					
					if not os.path.exists(os.path.join(dir, dircheck)):
						os.makedirs (os.path.join(dir, dircheck))
					
					if not os.path.isfile (os.path.join(dir,dircheck, filecheck[0])):
						save = open(os.path.join(dir,dircheck, filecheck[0]),"wb")
						save.write (self.file.read())
						save.close()
						self.subtitles_number = self.subtitles_number + 1
						output ("POBRANO PLIK: " + filecheck[0] + "\n")
					else:
						output ("PLIK ISTNIEJE: " + filecheck[0] + "\n")
			
		output ("ILOSC POBRANYCH PLIKOW: " + str(self.subtitles_number) + "\n")		
						
		return True

	
	def show (self):
		for order, link in enumerate (self.links):
			
			print str(order) + '.',
			for i in link:
				print i,
			
			print '\n'
	def kill (self):
		raise SystemError("PROCESS TERMINATED")
	

