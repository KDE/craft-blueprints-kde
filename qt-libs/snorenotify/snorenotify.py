# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["libs/qt5/qttools"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtwebsockets"] = None
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtspeech"] = None
        self.runtimeDependencies["libs/snoregrowl"] = None
        self.runtimeDependencies["dev-utils/snoretoast"] = None

    def setTargets(self):
        self.svnTargets['master'] = 'https://invent.kde.org/libraries/snorenotify.git'
        self.svnTargets['0.7'] = 'https://invent.kde.org/libraries/snorenotify.git|0.7'
        self.targetUpdatedRepoUrl["master"] = ("git://anongit.kde.org/snorenotify", "https://invent.kde.org/libraries/snorenotify.git")
        self.targetUpdatedRepoUrl["0.7"] = ("git://anongit.kde.org/snorenotify", "https://invent.kde.org/libraries/snorenotify.git")
        for ver in ['0.6.0', '0.7.0']:
            self.targets[ver] = "http://download.kde.org/stable/snorenotify/%s/src/snorenotify-%s.tar.xz" % (ver, ver)
            self.targetInstSrc[ver] = "snorenotify-%s" % ver
            self.targetDigestUrls[ver] = (
            "http://download.kde.org/stable/snorenotify/%s/src/snorenotify-%s.tar.xz.sha256" % (ver, ver),
            CraftHash.HashAlgorithm.SHA256)

        self.description = "Snorenotify is a multi platform Qt notification framework. Using a plugin system it is possible to create notifications with many different notification systems on Windows, Mac OS and Unix."
        self.patchLevel["0.7"] = 2
        self.defaultTarget = '0.7'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.staticArgs = "-DSNORE_STATIC=ON -DSNORE_STATIC_QT=ON"

