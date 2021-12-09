# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/KDAB/FatCRM.git"

        self.targets["2.4.0"] = "https://github.com/KDAB/FatCRM/releases/download/v2.4.0/fatcrm-2.4.0.tar.gz"
        self.archiveNames["2.4.0"] = "fatcrm-2.4.0.tar.gz"
        self.targetInstSrc["2.4.0"] = "fatcrm-2.4.0"
        self.targetDigests["2.4.0"] = (['ff3d5d84e137ac820de4f95ef14f6cf5e5ad40adee02eadb5082cb104de582ee'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "2.4.0"

        self.description = "Desktop Application for SugarCRM"
        self.webpage = "http://www.kdab.com/"
        self.displayName = "FatCRM"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
        self.runtimeDependencies["kde/pim/akonadi"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcontacts"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcalendarcore"] = None
        self.runtimeDependencies["kde/pim/akonadi-contacts"] = None
        self.runtimeDependencies["qt-libs/kdsoap"] = None
        self.runtimeDependencies["qt-libs/kdreports"] = None


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
