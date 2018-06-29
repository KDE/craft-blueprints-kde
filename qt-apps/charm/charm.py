# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/KDAB/Charm.git'
        self.defaultTarget = 'master'
        self.description = "The Cross-Platform Time Tracker"
        self.displayName = "Charm"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtwinextras"] = "default"
        self.runtimeDependencies["libs/qt5/qtmacextras"] = "default"
        self.runtimeDependencies["qt-libs/qtkeychain"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        self.defines["company"] = "Klarälvdalens Datakonsult AB"
        self.defines["executable"] = "bin\\Charm.exe"
        self.defines["license"] = os.path.join(self.sourceDir(), "License.txt")
        self.defines["icon"] = os.path.join(self.sourceDir(), "Charm", "Icons", "Charm.ico")
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")
        return TypePackager.createPackage(self)

