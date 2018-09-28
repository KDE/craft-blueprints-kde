# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qt3d"] = None
        self.runtimeDependencies["qt-libs/quazip"] = None
        self.runtimeDependencies["qt-libs/libjreen"] = None
        # self.runtimeDependencies["qt-libs/qtsparkle"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None
        # self.runtimeDependencies["qt-libs/qtweetlib"] = None
        self.runtimeDependencies["binary/vlc"] = None
        self.runtimeDependencies["kdesupport/qca"] = None
        self.runtimeDependencies["qt-libs/libechonest"] = None
        self.runtimeDependencies["kde/frameworks/tier1/attica"] = None
        self.runtimeDependencies["qt-libs/liblastfm"] = None
        self.runtimeDependencies["libs/luceneplusplus"] = None
        self.runtimeDependencies["libs/taglib"] = None
        self.runtimeDependencies["libs/gnutls"] = None
        self.buildDependencies["libs/websocketpp"] = None
        self.runtimeDependencies["libs/libsparsehash"] = None

    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/tomahawk-player/tomahawk.git'
        self.defaultTarget = 'master'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = " -DWITH_CRASHREPORTER=OFF -DBUILD_WITH_QT4=OFF -DWITH_KDE4=OFF -DBUILD_HATCHET=ON"
