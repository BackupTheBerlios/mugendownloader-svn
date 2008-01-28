#!/usr/bin/env python
# -*- coding: utf-8 -*-
# main.py
# Copyright (C) WoodenJesus 2007 <woodenjesus666@gmail.com>
# 
# mugendownlader.py is free software.
# 
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 2 of the License, or (at your option)
# any later version.
# 
# main.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with main.py.  If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.


__version__ = '0.2'

import inspect
import ctypes

import pygtk, gtk, gtk.glade, gobject
import ansidloader
import threading, time
import sys, os

### http://sebulba.wikispaces.com/recipe+thread2 killing thread	######

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble, 
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")
######################################################################

############### From pyGTK FAQ #######################################
def do_gui_operation(function, *args, **kw):
    def idle_func():
        gtk.threads_enter()
        try:
            function(*args, **kw)
            return False
        finally:
            gtk.threads_leave()
    gobject.idle_add(idle_func)
#####################################################################


#run download thread

class RunDload ( threading.Thread ):
	
	def __init__ (self, window, args=[]):
		threading.Thread.__init__(self)
		self.args = args
		self.work = threading.Event()
		self.window = window
		#print self.args

	def run (self):
		self.work.set()
		self.download = ansidloader.AnsiDloader()
		self.download.findsub(*self.args)
		do_gui_operation (self.window.Finish)
		self.work.clear()
		#self.join()
	
	def stop(self):
		self.work.clear()
		self.terminate()
		self.join()


### http://sebulba.wikispaces.com/recipe+thread2 killing thread	######
	def _get_my_tid(self):
		"""determines this (self's) thread id"""
		if not self.isAlive():
			raise threading.ThreadError("the thread is not active")
        
        # do we have it cached?
		if hasattr(self, "_thread_id"):
			return self._thread_id
        
        # no, look for it in the _active dict
		for tid, tobj in threading._active.items():
			if tobj is self:
				self._thread_id = tid
				return tid
        
		raise AssertionError("could not determine the thread's id")
        
	def raise_exc(self, exctype):
		"""raises the given exception type in the context of this thread"""
		_async_raise(self._get_my_tid(), exctype)
    
	def terminate(self):
		"""raises SystemExit in the context of the given thread, which should 
		cause the thread to exit silently (unless caught)"""
		self.raise_exc(SystemExit)
######################################################################

#initialize main window
class MugenWindow:

	def __init__(self):

		self.glade = gtk.glade.XML("interface.glade")
		self.window = self.glade.get_widget('main')
		
		self.exit = self.glade.get_widget('close')
		self.exit.connect("clicked", self.Exit)
		self.window.connect ("destroy", self.Exit)
			
		self.about = self.glade.get_widget('about')
		self.about.connect("clicked", self.About)
		
		self.ok = self.glade.get_widget('ok')
		self.ok.connect("clicked", self.Download)
		
		self.cancel = self.glade.get_widget('cancel')
		self.cancel.connect("clicked", self.CancelDownload)
		
		self.find = self.glade.get_widget('find')
		self.dirchooser = self.glade.get_widget('dirchooser')
		self.dirchooser.connect("selection-changed", self.UpdateDefault)
		self.cancel.connect("clicked", self.CancelDownload)
		self.pageno = self.glade.get_widget('pageno')
		self.output = self.glade.get_widget('output')
		
		if os.path.isfile ('default.conf'):
			default = open ('default.conf', 'r')
			dir = default.read()
			if os.path.isdir (dir):
				self.dirchooser.set_filename(dir)
			default.close()
		
		self.text = self.output.get_buffer()
		self.download = RunDload (self.window, (self.find.get_text(), self.dirchooser.get_filename(), self.OutputHandler))
		
		self.window.show()

	def UpdateDefault(self, *trash):
		if os.path.isfile ('default.conf'):
			os.remove ('default.conf')
		default = open ('default.conf', 'w')
		default.write(self.dirchooser.get_filename())
		default.close()
		
	def Download (self, button):
		if not self.download.work.isSet():
			if self.find.get_text() != '':
				self.download = RunDload (self, (self.find.get_text(), self.dirchooser.get_filename(),  self.OutputHandler, self.pageno.get_value() ))
				self.ok.hide()
				self.cancel.show()
				self.download.start()
	
	def Finish (self):
		self.cancel.hide()
		self.ok.show()
	
	def CancelDownload (self, button):
		if self.download.work.isSet():
			self.download.stop()
			self.cancel.hide()
			self.ok.show()
			
	def About (self, *arg):
		dialog = gtk.AboutDialog()                                                                                                                                                                     
		dialog.set_name("Mugen ∞ Downloader " + __version__)                                                                                                                                                                  
		dialog.set_copyright("WoodenJesus")
		dialog.set_comments("Feyd Rautha strikes back")                                                                                                                                    
		dialog.set_website("http://mugendownloader.berlios.de")                                                                                                                                                   
        
        ## Close dialog on user response                                                                                                                                                               
		dialog.connect ("response", lambda d, r: d.destroy())                                                                                                                                          
		dialog.show() 



	def Exit(self, *arg):
		sys.exit(0)	
	
	def LOL	(self, *args):
		self.aboutwindow.hide()
		
	def OutputHandler (self, string):
		self.output.scroll_to_iter(self.text.get_end_iter(), 0)
		self.text.insert (self.text.get_end_iter(), string)
		self.output.scroll_to_iter(self.text.get_end_iter(), 0)
		
def main():
	gtk.gdk.threads_init()
	gtk.gdk.threads_enter()
	run = MugenWindow()
	gtk.main()
	gtk.gdk.threads_leave()

main()
