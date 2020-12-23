# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "A storage service for PIM data and meta data"

    def registerOptions(self):
        self.options.dynamic.registerOption("useDesignerPlugin", True)

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["libs/boost/boost-graph"] = None
        self.runtimeDependencies["libs/libxslt"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["libs/shared-mime-info"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        if self.options.dynamic.useDesignerPlugin:
            self.runtimeDependencies["kde/frameworks/tier3/kdesignerplugin"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DUSE_UNITY_CMAKE_SUPPORT=ON "
        self.subinfo.options.configure.args = "-DDATABASE_BACKEND=SQLITE -DAKONADI_RUN_MYSQL_ISOLATED_TESTS=OFF -DBUILD_TESTING=OFF "

        if not self.subinfo.options.dynamic.useDesignerPlugin:
            self.subinfo.options.configure.args += "-DBUILD_DESIGNERPLUGIN=OFF "
