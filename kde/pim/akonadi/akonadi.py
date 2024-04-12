# -*- coding: utf-8 -*-
import info
from Blueprints.CraftPackageObject import CraftPackageObject


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
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildTests = False
        self.subinfo.options.configure.args += ["-DUSE_UNITY_CMAKE_SUPPORT=ON", "-DDATABASE_BACKEND=SQLITE", "-DAKONADI_RUN_MYSQL_ISOLATED_TESTS=OFF"]

        if not self.subinfo.options.dynamic.useDesignerPlugin:
            self.subinfo.options.configure.args += ["-DBUILD_DESIGNERPLUGIN=OFF"]
