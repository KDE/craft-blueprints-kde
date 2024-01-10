# -*- coding: utf-8 -*-
import info
from Blueprints.CraftPackageObject import CraftPackageObject
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.displayName = "Konversation"
        self.description = "a KDE based irc client"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kbookmarks"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
            self.runtimeDependencies["kde/frameworks/tier3/kemoticons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kidletime"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kpackage"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier1/solid"] = None
        self.runtimeDependencies["kde/frameworks/tier1/sonnet"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kdesupport/qca"] = None
        self.runtimeDependencies["qt-libs/phonon"] = None

        if not CraftCore.compiler.isWindows:
            self.runtimeDependencies["kde/frameworks/tier3/kglobalaccel"] = None


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")

    def createPackage(self):
        self.defines["executable"] = "bin\\konversation.exe"
        self.defines["icon"] = os.path.join(self.blueprintDir(), "konversation.ico")

        self.ignoredPackages.append("binary/mysql")

        return super().createPackage()
