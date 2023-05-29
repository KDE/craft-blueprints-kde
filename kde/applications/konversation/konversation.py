# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *
from Packager.CollectionPackagerBase import PackagerLists


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.displayName = "Konversation"
        self.description = "a KDE based irc client"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kbookmarks"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
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
        CMakePackageBase.__init__(self)
        self.blacklist_file = [PackagerLists.runtimeBlacklist, os.path.join(self.packageDir(), "blacklist.txt")]

    def createPackage(self):
        self.defines["executable"] = "bin\\konversation.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "konversation.ico")

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)
