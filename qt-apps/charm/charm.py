# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.registerOption("update_check_url", "")

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/KDAB/Charm.git"
        for ver in ["1.12.0"]:
            self.targets[ver] = f"https://github.com/KDAB/Charm/archive/{ver}.tar.gz"
            self.archiveNames[ver] = f"charm-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"Charm-{ver}"
        self.defaultTarget = "1.12.0"

        self.description = "The Cross-Platform Time Tracker"
        self.displayName = "Charm"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtwinextras"] = None
        self.runtimeDependencies["libs/qt5/qtmacextras"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
        if self.subinfo.buildTarget != "master":
            self.subinfo.options.configure.args = f"-DCharm_VERSION={self.subinfo.buildTarget}"
        if self.subinfo.options.dynamic.update_check_url:
            self.subinfo.options.configure.args += [f"-DUPDATE_CHECK_URL={self.subinfo.options.dynamic.update_check_url}"]

    def createPackage(self):
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        self.defines["company"] = "Klarälvdalens Datakonsult AB"
        self.defines["executable"] = "bin\\Charm.exe"
        self.defines["license"] = os.path.join(self.sourceDir(), "License.txt")
        self.defines["icon"] = os.path.join(self.sourceDir(), "Charm", "Icons", "Charm.ico")
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")
        return super().createPackage()
