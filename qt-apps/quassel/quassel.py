# -*- coding: utf-8 -*-

import info
from CraftOS.osutils import OsUtils
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/quassel/quassel.git"
        for ver in ["0.12.0", "0.12.2", "0.12.4"]:
            self.targets[ver] = f"http://quassel-irc.org/pub/quassel-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"quassel-{ver}"
        self.targetDigests["0.12.2"] = "12e9a88597f724498c40a1548b5f788e7c40858c"
        self.patchToApply["0.11.0"] = ("quassel-0.11.0-20141002.diff", 1)

        self.webpage = "http://quassel-irc.org"
        self.description = "a distributed IRC client"
        self.defaultTarget = "0.12.4"

    def setDependencies(self):
        self.runtimeDependencies["qt-libs/snorenotify"] = "default"
        self.runtimeDependencies["libs/zlib"] = "default"
        self.runtimeDependencies["libs/openssl"] = "default"
        # self.runtimeDependencies["kdesupport/qca"] = "default"
        self.runtimeDependencies["dev-utils/pkg-config"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebengine"] = "default"
        self.runtimeDependencies["libs/qt5/qtscript"] = "default"
        self.buildDependencies["libs/qt5/qttools"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/sonnet"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.supportsNinja = False
        self.subinfo.options.configure.args = " -DUSE_QT5=ON -DCMAKE_DISABLE_FIND_PACKAGE_Qt5DBus=ON"
        if CraftCore.compiler.isMSVC2017():
            self.subinfo.options.configure.args += " -DCMAKE_CXX_FLAGS=\"-std:c++17\""

    def install(self):
        if not CMakePackageBase.install(self):
            return False
        if OsUtils.isWin():
            os.makedirs(os.path.join(self.installDir(), "bin"))
            shutil.move(os.path.join(self.installDir(), "quassel.exe"),
                        os.path.join(self.installDir(), "bin", "quassel.exe"))
            shutil.move(os.path.join(self.installDir(), "quasselcore.exe"),
                        os.path.join(self.installDir(), "bin", "quasselcore.exe"))
            shutil.move(os.path.join(self.installDir(), "quasselclient.exe"),
                        os.path.join(self.installDir(), "bin", "quasselclient.exe"))
        return True

    def preArchive(self):
        return utils.mergeTree(os.path.join(self.archiveDir(), "bin"), self.archiveDir())

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist.txt"))
        self.defines["gitDir"] = self.sourceDir()
        self.defines["caption"] = self.binaryArchiveName(fileType=None).capitalize()
        self.defines["productname"] = None
        self.defines["company"] = None

        self.scriptname = os.path.join(self.sourceDir(), "scripts", "build", "NullsoftInstaller.nsi")
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")


        return TypePackager.createPackage(self)
