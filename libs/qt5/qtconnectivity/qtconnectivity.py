# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        if CraftCore.compiler.isAndroid:
            for ver in self.versionInfo.tarballs() + self.versionInfo.branches() + self.versionInfo.tags():
                qtVer = CraftVersion(ver)
                if ver == "dev":
                    self.patchToApply[ver] = []
                elif ver == "kde/5.15":
                    self.patchToApply[ver] = [
                        ("android-30-permissions.diff", 1), # Ensures that correct permissions are checked depending on sdk version
                    ]
                elif qtVer >= "5.15.2":
                    self.patchToApply[ver] = [
                        ("android-30-permissions.diff", 1), # Ensures that correct permissions are checked depending on sdk version
                    ]
            self.patchLevel["5.15.2"] = 1
            self.patchLevel["5.15.5"] = 1
            self.patchLevel["kde/5.15"] = 1


    def setDependencies(self):
        if CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/qt5/qtandroidextras"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Package.Qt5CorePackageBase import *


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)
