'''
  This file is part of the PyPhantomJS project.

  Copyright (C) 2011 James Roe <roejames12@hotmail.com>

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import sys

import sip
from PyQt4.QtCore import (pyqtProperty, pyqtSlot, QObject,
                          QFile)
from PyQt4.QtGui import QApplication
from PyQt4.QtNetwork import QNetworkProxy, QNetworkProxyFactory

from __init__ import __version_info__
from utils import injectJsInFrame
from plugincontroller import do_action
from webpage import WebPage
from networkaccessmanager import NetworkAccessManager
from filesystem import FileSystem
from encoding import Encode


class Phantom(QObject):
    def __init__(self, parent, args):
        QObject.__init__(self, parent)

        # variable declarations
        self.m_defaultPageSettings = {}
        self.m_pages = []
        self.m_verbose = args.verbose
        self.m_page = WebPage(self)
        self.m_returnValue = 0
        self.m_terminated = False
        # setup the values from args
        self.m_scriptFile = args.script
        self.m_args = args.script_args
        self.m_scriptEncoding = Encode(args.script_encoding, 'utf-8')
        self.m_outputEncoding = Encode(args.output_encoding, sys.stdout.encoding_sys)

        self.m_filesystem = FileSystem(self)

        self.m_pages.append(self.m_page)

        do_action('PhantomInitPre')

        if args.proxy is None:
            QNetworkProxyFactory.setUseSystemConfiguration(True)
        else:
            proxy = QNetworkProxy(QNetworkProxy.HttpProxy, args.proxy[0], int(args.proxy[1]))
            QNetworkProxy.setApplicationProxy(proxy)

        # Provide WebPage with a non-standard Network Access Manager
        self.m_netAccessMan = NetworkAccessManager(self, args.auth, args.cookies, args.disk_cache, args.ignore_ssl_errors)
        self.m_page.setNetworkAccessManager(self.m_netAccessMan)

        self.m_page.javaScriptConsoleMessageSent.connect(self.printConsoleMessage)

        self.m_defaultPageSettings['loadImages'] = args.load_images
        self.m_defaultPageSettings['loadPlugins'] = args.load_plugins
        self.m_defaultPageSettings['javascriptEnabled'] = True
        self.m_defaultPageSettings['XSSAuditingEnabled'] = False
        self.m_defaultPageSettings['userAgent'] = self.m_page.userAgent()
        self.m_defaultPageSettings['localAccessRemote'] = args.local_access_remote
        self.m_page.applySettings(self.m_defaultPageSettings)

        self.libraryPath = os.path.dirname(os.path.abspath(self.m_scriptFile))

        # inject our properties and slots into javascript
        self.m_page.mainFrame().addToJavaScriptWindowObject('phantom', self)
        self.m_page.mainFrame().addToJavaScriptWindowObject('fs', self.m_filesystem)

        jsShims = (
            ':/filesystem-shim.js',
            ':/webpage-shim.js'
        )
        for shim in jsShims:
            f = QFile(shim)
            if not f.open(QFile.ReadOnly):
                sys.exit("Failed to load shim '%s'" % shim)

            f = str(f.readAll())
            if not f:
                sys.exit("Failed to load shim '%s'" % shim)
            self.m_page.mainFrame().evaluateJavaScript(f)

        do_action('PhantomInitPost')

    def execute(self):
        injectJsInFrame(self.m_scriptFile, self.m_scriptEncoding.encoding, os.path.dirname(os.path.abspath(__file__)), self.m_page.mainFrame(), True)
        return not self.m_terminated

    def printConsoleMessage(self, message, lineNumber, source):
        if source:
            message = '%s:%d %s' % (source, lineNumber, message)
        print message

    def returnValue(self):
        return self.m_returnValue

    ##
    # Properties and methods exposed to JavaScript
    ##

    @pyqtProperty('QStringList')
    def args(self):
        return self.m_args

    @pyqtSlot(result=WebPage)
    def createWebPage(self):
        page = WebPage(self)
        self.m_pages.append(page)
        page.applySettings(self.m_defaultPageSettings)
        page.setNetworkAccessManager(self.m_netAccessMan)
        page.libraryPath = os.path.dirname(os.path.abspath(self.m_scriptFile))
        return page

    @pyqtProperty('QVariantMap')
    def defaultPageSettings(self):
        return self.m_defaultPageSettings

    @pyqtSlot()
    @pyqtSlot(int)
    def exit(self, code=0):
        self.m_terminated = True
        self.m_returnValue = code

        # stop javascript execution in start script;
        # delete all the pages C++ objects, then clear
        # the page list, and empty the Phantom page
        for page in self.m_pages:
            sip.delete(page)
        del self.m_pages[:]
        self.m_page = None

        QApplication.instance().exit(code)

    @pyqtSlot(str, result=bool)
    def injectJs(self, filePath):
        return injectJsInFrame(filePath, self.m_scriptEncoding.encoding, self.libraryPath, self.m_page.mainFrame())

    @pyqtProperty(str)
    def libraryPath(self):
        return self.m_page.libraryPath

    @libraryPath.setter
    def libraryPath(self, dirPath):
        self.m_page.libraryPath = dirPath

    @pyqtProperty(str)
    def outputEncoding(self):
        return self.m_outputEncoding.name

    @outputEncoding.setter
    def outputEncoding(self, encoding):
        self.m_outputEncoding = Encode(encoding, self.m_outputEncoding.encoding)

        sys.stdout.encoding = self.m_outputEncoding.encoding
        sys.stdout.encode_to = self.m_outputEncoding.encoding
        sys.stderr.encoding = self.m_outputEncoding.encoding
        sys.stdout.encode_to = self.m_outputEncoding.encoding

    @pyqtProperty(str)
    def scriptName(self):
        return os.path.basename(self.m_scriptFile)

    @pyqtProperty('QVariantMap')
    def version(self):
        version = {
            'major': __version_info__[0],
            'minor': __version_info__[1],
            'patch': __version_info__[2]
        }
        return version

    do_action('Phantom')
