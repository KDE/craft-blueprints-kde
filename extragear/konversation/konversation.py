# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["1.7"] = "https://invent.kde.org/network/konversation.git|1.7"
        self.svnTargets["master"] = "https://invent.kde.org/network/konversation.git"
        self.targetUpdatedRepoUrl["1.7"] = ("https://anongit.kde.org/konversation", "https://invent.kde.org/network/konversation.git|1.7")
        self.targetUpdatedRepoUrl["master"] = ("https://anongit.kde.org/konversation", "https://invent.kde.org/network/konversation.git")
        for ver in ["1.7.4", "1.7.5"]:
            self.targets[ver] = "http://download.kde.org/stable/konversation/%s/src/konversation-%s.tar.xz" % (ver, ver)
            self.targetInstSrc[ver] = "konversation-%s" % ver
        self.defaultTarget = "1.7.5"

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
        if self.buildTarget == "master":
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


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(self.packageDir(), "blacklist.txt")
        ]

    def createPackage(self):
        self.defines["executable"] = "bin\\konversation.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "konversation.ico")

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)
