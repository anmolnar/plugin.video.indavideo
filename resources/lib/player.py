# -*- coding: utf-8 -*-

import re,sys,json,time,xbmc

from resources.lib import control


class player(xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)


    def run(self, name, url, poster, link):
        try:
            self.loadingTime = time.time()
            self.totalTime = 0 ; self.currentTime = 0

            self.link = link

            item = control.item(path=url, iconImage='DefaultVideo.png', thumbnailImage=poster)
            item.setInfo(type='Video', infoLabels = {'title': name})
            try: item.setArt({'poster': poster})
            except: pass
            item.setProperty('Video', 'true')
            #item.setProperty('IsPlayable', 'true')
            handle = int(sys.argv[1])
            control.player.play(url, item)
            control.resolve(int(sys.argv[1]), True, item)

            self.keepPlaybackAlive()

        except:
            return


    def keepPlaybackAlive(self):
        pname = '%s.player.overlay' % control.addonInfo('id')
        control.window.clearProperty(pname)

        for i in range(0, 240):
            if self.isPlayingVideo(): break
            xbmc.sleep(1000)
        
        while self.isPlayingVideo():
            try:
                self.totalTime = self.getTotalTime()
                self.currentTime = self.getTime()

                watcher = (self.currentTime / self.totalTime >= .9)
                property = control.window.getProperty(pname)

                if watcher == True and not property == '7':
                    control.window.setProperty(pname, '7')
                    self.markEpisodeDuringPlayback('7')
            except:
                pass
            xbmc.sleep(2000)

        control.window.clearProperty(pname)


    def onPlayBackStarted(self):
        self.idleForPlayback()

    
    def idleForPlayback(self):
        for i in range(0, 200):
            if control.condVisibility('Window.IsActive(busydialog)') == 1: control.idle()
            else: break
            control.sleep(100)


    def markEpisodeDuringPlayback(self, watched):
        try:
            if not int(watched) == 7: raise Exception()
            from resources.lib import localplaycount
            localplaycount.addPlaycount(self.link)
        except:
            pass