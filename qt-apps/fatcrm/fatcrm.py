# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/KDAB/FatCRM.git"
        self.defaultTarget = "master"

        self.description = "Desktop Application for SugarCRM"
        self.webpage = "http://www.kdab.com/"
        self.displayName = "FatCRM"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = "default"
        self.runtimeDependencies["kde/pim/akonadi"] = "default"
        self.runtimeDependencies["kde/pim/kcontacts"] = "default"
        self.runtimeDependencies["kde/pim/kcalcore"] = "default"
        self.runtimeDependencies["kde/pim/akonadi-contacts"] = "default"
        self.runtimeDependencies["qt-libs/kdsoap"] = "default"
        self.runtimeDependencies["qt-libs/kdreports"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.defines["company"] = "Klarälvdalens Datakonsult AB"
        self.defines["executable"] = "bin\\fatcrm.exe"
        self.defines["license"] = os.path.join(self.sourceDir(), "LICENSE.GPL.txt")
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        self.ignoredPackages.append("binary/mysql")
        return TypePackager.createPackage(self)
