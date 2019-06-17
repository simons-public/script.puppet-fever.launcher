import os
import sys
import subprocess
import time
import shutil
import xbmc
import xbmcaddon
import xbmcgui

import SimpleDownloader as downloader

addon = xbmcaddon.Addon(id='script.puppet-fever.launcher')
addonPath = addon.getAddonInfo('path')
addonIcon = addon.getAddonInfo('icon')
addonVersion = addon.getAddonInfo('version')
dialog = xbmcgui.Dialog()
language = addon.getLocalizedString
scriptid = 'script.puppet-fever.launcher'
downloader = downloader.SimpleDownloader()

def log(msg):
    """ Logging """
    msg = msg.encode('utf-8')
    xbmc.log('%s: %s' % (scriptid, msg))

def which(appname):
    """ Returns the full path of an executable in $PATH """
    for path in os.environ['PATH'].split(os.pathsep):
        fullpath = os.path.join(path, appname)
        if os.path.exists(fullpath) and os.access(fullpath, os.X_OK):
            return fullpath
    return None

def getAddonDataPath():
    path = xbmc.translatePath('special://profile/addon_data/%s' % scriptid).decode("utf-8")
    if not os.path.exists(path):
        log('addon userdata folder does not exist, creating: %s' % path)
        try:
            os.makedirs(path)
            log('created directory: %s' % path)
        except:
            log('ERROR: failed to create directory: %s' % path)
            dialog.notification(language(50212), language(50215), addonIcon, 5000)
    return path

def checkForWine():
    """ Ensure wine is available, or stop addon """
    wine_bin = which('wine')

    if not wine_bin:
        # Wine Required
        log(language(50011))
        dialog.ok(language(50010), language(50011)) 
        sys.exit()

def checkForApp():
    """ Check for the app, download if not existing """
    data_path = getAddonDataPath()

    if not os.path.exists(os.path.join(data_path, 'Puppet Fever Companion')):
        log(language(50013))
        dialog.ok(language(50012), language(50013))

        params = {"url": "https://storage.googleapis.com/puppetfever.coffeestainstudios.com/pfcompanion.zip",
                  "download_path": "/tmp"}
        downloader.download("pfcompanion.zip", params)
        xbmc.executebuiltin("XBMC.Extract(" + '/tmp/pfcompanion.zip' + ',' + data_path + ')', True)

def runApp():
    """ Run the app with wine """
    data_path = getAddonDataPath()
    wine_bin = which('wine')
    exe_path = os.path.join(data_path, 'Puppet Fever Companion', 'Puppet Fever.exe')

    subprocess.call([wine_bin, exe_path])

log('Launching Puppet Fever Companion App')
checkForWine()
checkForApp()
runApp()
