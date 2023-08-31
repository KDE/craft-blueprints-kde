# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/libraries/upnp-lib-qt.git"

        self.defaultTarget = "master"
        self.description = "A Qt-based client-side and server-side UPnP library"
        self.displayName = "UPnP-Qt-lib"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["qt-libs/kdsoap"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
