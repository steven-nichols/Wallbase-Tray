#!/usr/bin/env python
import os.path
import string
from DetectOS import DetectOS

def SetWallpaper(Path):
    """Force the desktop to redraw the wallpaper"""
    
    if not os.path.exists(Path):
        print "Path not found"
        return
    
    # Detect which OS we are running
    # MS Windows
    myos = DetectOS()
    if myos == 'windows':
        print "Windows"
        # Wallpaper path stored in "HKEY_CURRENT_USER\Control Panel\Desktop\Wallpaper"
        hKey = _winreg.OpenKey (_winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, _winreg.KEY_SET_VALUE)
        _winreg.SetValueEx(hKey, "Wallpaper", 0,_winreg.REG_SZ, Path)
        
        # http://mail.python.org/pipermail/python-list/2005-July/330379.html
        #shutil.copyfile(os.path.join(images_dir, wallpaper[0].find('file').text), wallpaperfile)
        # Refresh the desktop
        SPI_SETDESKWALLPAPER = 20 # According to http://support.microsoft.com/default.aspx?scid=97142
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, Path, 0)
        #cs = ctypes.c_buffer(output_file)
        #ctypes.windll.user32.SystemParametersInfoA(win32con.SPI_SETDESKWALLPAPER,0,output_file,0)
        #win32gui.SystemParametersInfo (win32con.SPI_SETDESKWALLPAPER, bmp_path, win32con.SPIF_SENDCHANGE)
        #os.system('RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters ,1 ,True')
    # Mac OS X
    elif myos == 'mac':
        # http://stackoverflow.com/questions/431205/how-can-i-programatically-change-the-background-in-mac-os-x#431273
        import subprocess

        SCRIPT = """/usr/bin/osascript<<END
        tell application "Finder"
        set desktop picture to POSIX file "%s"
        end tell
        END"""

        subprocess.Popen(SCRIPT % Path, shell=True)
    # Linux Gnome
    elif myos == 'gnome':
        # http://www.tuxradar.com/content/code-project-use-weather-wallpapers
        cmd = string.join(["gconftool-2 -s /desktop/gnome/background/picture_filename -t string \"",Path,"\""],'')
        os.system(cmd)
    # Linus KDE
    elif myos == 'kde': 
            if os.getenv('KDE_SESSION_VERSION') == '':
                # KDE 3.5
                cmd = "dcop kdesktop KBackgroundIface setWallpaper %s 6" % Path
                os.system(cmd)
            else:
                print "KDE 4.x currently has no way to set the wallpaper from the command line. Sorry."
    else:
        print "unsupported OS"
