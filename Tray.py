#!/usr/bin/env python

import os
import gtk
import gobject
import thread
from threading import Thread

from Wallbase import Wallbase
from Settings import WALLBASE_ALL_SFW, WALLBASE_ANIME_SFW, WALLBASE_GENERAL_SFW

class TrackerStatusIcon(gtk.StatusIcon):
    def __init__(self):
        gtk.StatusIcon.__init__(self)
        menu = '''
            <ui>
             <menubar name="Menubar">
              <menu action="Menu">
               <menuitem action="Next"/>
               <menuitem action="Pause"/>
               <menuitem action="Prev"/>
               <menuitem action="Save"/>
               <separator/>
               <menuitem action="1minute"/>
               <menuitem action="5minutes"/>
               <menuitem action="15minutes"/>
               <separator/>
               <menuitem action="AllSFW"/>
               <menuitem action="AnimeSFW"/>
               <menuitem action="GeneralSFW"/>
               <separator/>
               <menuitem action="About"/>
               <menuitem action="Quit"/>
              </menu>
             </menubar>
            </ui>
        '''
        actions = [
            ('Menu',  None, 'Menu'),
            ('Next', None, '_Next', None, 'Search files with MetaTracker', self.on_next),
            ('Pause', None, '_Pause', None, 'Change MetaTracker preferences', self.on_pause),
            ('Prev', None, 'Pre_vious', None, 'Change MetaTracker preferences', self.on_prev),
            ('Save', None, '_Save Image', None, 'Change MetaTracker preferences', self.on_saveimg),
            ('1minute', None, '1 minute', None, 'Search files with MetaTracker', self.on_1min),
            ('5minutes', None, '5 minutes', None, 'Change MetaTracker preferences', self.on_5min),
            ('15minutes', None, '15 minutes', None, 'Change MetaTracker preferences', self.on_15min),
            ('AllSFW', None, '_All (SFW)', None, 'Search files with MetaTracker', self.on_allsfw),
            ('AnimeSFW', None, 'A_nime (SFW) ', None, 'Change MetaTracker preferences', self.on_animesfw),
            ('GeneralSFW', None, '_General (SFW)', None, 'Change MetaTracker preferences', self.on_generalsfw),
            ('About', gtk.STOCK_ABOUT, 'About', None, 'About MetaTracker', self.on_about),
            ('Quit', None, '_Quit', None, None, self.on_quit)]
        ag = gtk.ActionGroup('Actions')
        ag.add_actions(actions)
        self.manager = gtk.UIManager()
        self.manager.insert_action_group(ag, 0)
        self.manager.add_ui_from_string(menu)
        self.menu = self.manager.get_widget('/Menubar/Menu/About').props.parent
        search = self.manager.get_widget('/Menubar/Menu/Search')
        #search.get_children()[1].set_from_stock(gtk.STOCK_FIND, gtk.ICON_SIZE_MENU)
        #self.set_from_stock(gtk.STOCK_FIND)
        self.set_from_file("fav.gif")
        self.set_tooltip('Tracker Desktop Search')
        self.set_visible(True)
        self.connect('activate', self.on_next)
        self.connect('popup-menu', self.on_popup_menu)
        self.wallbase = Wallbase()
        #self.wallbase.getNext()
        self.timeout = 60*1000 # 1 minute timer
        self.timer = None
        self.set_timeout() # start the timer


    def set_timeout(self):
        if self.timer is not None:
            gobject.source_remove(self.timer)
        self.timer = gobject.timeout_add(self.timeout, self.my_timer) # call every min

    def on_popup_menu(self, status, button, time):
        self.menu.popup(None, None, None, button, time)
    
    def on_saveimg(self, data):
        dialog = gtk.FileChooserDialog("Save as...", None, gtk.FILE_CHOOSER_ACTION_SAVE, 
                (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_current_name(os.path.basename(self.wallbase.getCurrentWallpaper()))
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            print 'ok'
            print dialog.get_filename()
            self.wallbase.saveImage(os.path.join(dialog.get_current_folder(), dialog.get_filename()))
        else:
            print 'not ok'
        dialog.destroy()
        
    def on_next(self, data):
        #thread.start_new_thread(self.wallbase.getNext, ())
        self.notification("Wallbase Tray", "Fetching new wallpaper")
        self.wallbase.getNext()
        
    def on_prev(self, data):
        self.wallbase.getPrevious()

    def on_pause(self, data):
        print "pause"
        gobject.source_remove(self.timer)        
        	    
    def on_1min(self, data):
        self.timeout = 60*1000 # 1 minute
        self.set_timeout()
        print "Set for 1 minute"
        
    def on_5min(self, data):
        self.timeout = 5*60*1000 # 5 minutes
        self.set_timeout()
        print "Set for 5 minutes"
    
    def on_15min(self, data):
        self.timeout = 15*60*1000 # 5 minutes
        self.set_timeout()
        print "Set for 15 minutes"
        
    def on_allsfw(self, data):
        self.wallbase.setSearchURL(WALLBASE_ALL_SFW)
        print "Switch to All (SFW)"
        
    def on_animesfw(self, data):
        self.wallbase.setSearchURL(WALLBASE_ANIME_SFW)
        print "Switch to Anime (SFW)"
    
    def on_generalsfw(self, data):
        self.wallbase.setSearchURL(WALLBASE_GENERAL_SFW)
        print "Switch to General (SFW)"
        
    def on_about(self, data):
        dialog = gtk.AboutDialog()
        dialog.set_name('Wallbase Changer')
        dialog.set_version('0.1.0')
        dialog.set_comments('A desktop wallpaper changer')
        #dialog.set_website('www.freedesktop.org/Tracker')
        dialog.run()
        dialog.destroy()

    def on_quit(self, data):
        self.wallbase.cleanUp()
        gtk.main_quit()

    def my_timer(self):
        self.notification("Wallbase Tray", "Fetching new wallpaper")
        self.wallbase.getNext()
        return True
    
    def notification(self, title, message):
        try:
            import pynotify
            if pynotify.init("Wallbase Tray"):
                n = pynotify.Notification(title, message)
                n.show()
            else:
                print "there was a problem initializing the pynotify module"
        except:
            print "you don't seem to have pynotify installed"    
    
if __name__ == '__main__':
	TrackerStatusIcon()
	gtk.main()


