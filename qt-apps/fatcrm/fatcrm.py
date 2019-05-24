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
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
        self.runtimeDependencies["kde/pim/akonadi"] = None
        self.runtimeDependencies["kde/pim/kcontacts"] = None
        self.runtimeDependencies["kde/pim/kcalcore"] = None
        self.runtimeDependencies["kde/pim/akonadi-contacts"] = None
        self.runtimeDependencies["qt-libs/kdsoap"] = None
        self.runtimeDependencies["qt-libs/kdreports"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.defines["company"] = "Klarälvdalens Datakonsult AB"
        if CraftCore.compiler.isMacOS:
            self.defines["executable"] = "Applications/KDE/fatcrm.app"
        else:
            self.defines["executable"] = "bin\\fatcrm.exe"
        self.defines["license"] = os.path.join(self.sourceDir(), "LICENSE.GPL.txt")
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        self.ignoredPackages.append("binary/mysql")
        return TypePackager.createPackage(self)
