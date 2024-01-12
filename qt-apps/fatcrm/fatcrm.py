# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/KDAB/FatCRM.git"

        self.targets["2.5.0"] = "https://github.com/KDAB/FatCRM/releases/download/v2.5.0/fatcrm-2.5.0.tar.gz"
        self.archiveNames["2.5.0"] = "fatcrm-2.5.0.tar.gz"
        self.targetInstSrc["2.5.0"] = "fatcrm-2.5.0"
        self.targetDigests["2.5.0"] = (["662b7c5ccfe455f64e1058c1ec5f26968944d7bb0f9380b950bd11bf2c1a7ec3"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "2.5.0"

        self.description = "Desktop Application for SugarCRM"
        self.webpage = "https://www.kdab.com/"
        self.displayName = "FatCRM"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
        self.runtimeDependencies["kde/pim/akonadi"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcontacts"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcalendarcore"] = None
        self.runtimeDependencies["kde/pim/akonadi-contacts"] = None
        self.runtimeDependencies["qt-libs/kdsoap"] = None
        self.runtimeDependencies["qt-libs/kdreports"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()

    def createPackage(self):
        self.defines["company"] = "Klarälvdalens Datakonsult AB"
        self.defines["executable"] = "bin\\fatcrm.exe"
        self.defines["license"] = os.path.join(self.sourceDir(), "LICENSE.GPL.txt")
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        self.ignoredPackages.append("binary/mysql")
        return super().createPackage()
