# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        for ver in self.versionInfo.tarballs() + self.versionInfo.branches() + self.versionInfo.tags():
            qtVer = CraftVersion(ver)
            if qtVer >= CraftVersion("5.9"):
                self.patchToApply[ver] = [("0001-Fix-the-detection-of-python2.exe.patch", 1)]#https://codereview.qt-project.org/#/c/203000/

    def setDependencies(self):
        self.buildDependencies["dev-utils/gperf"] = "default"
        self.buildDependencies["dev-utils/python2"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtlocation"] = "default"
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebchannel"] = "default"


from Package.Qt5CorePackageBase import *


class QtPackage(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True
        # sources on different partitions other than the one of the build dir
        # fails. some submodules fail even with the common shadow build...
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.needsShortPath = True

    def fetch(self):
        if isinstance(self, GitSource):
            utils.system(["git", "clean", "-xdf"], cwd=self.sourceDir())
        return Qt5CorePackageBase.fetch(self)

    def compile(self):
        env = {}
        if CraftCore.compiler.isMacOS:
            # we need mac's version of libtool here
            env["PATH"] = f"/usr/bin/:{os.environ['PATH']}"
        if self.qtVer < CraftVersion("5.9") and CraftCore.compiler.isWindows:
            env["PATH"] = CraftCore.settings.get("Paths", "PYTHON27") + ";" + os.environ["PATH"]
        with utils.ScopedEnv(env):
            return Qt5CorePackageBase.compile(self)

    def install(self):
        if not Qt5CorePackageBase.install(self):
            return False

        if CraftCore.compiler.isWindows and os.path.isdir(os.path.join(self.imageDir(), "resources")):
            # apply solution for wrong install location of some important files
            # see: https://stackoverflow.com/a/35448081
            utils.mergeTree(os.path.join(self.imageDir(), "resources"),
                            os.path.join(self.imageDir(), "bin"))
        return True


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage, condition=not CraftCore.compiler.isMinGW())
