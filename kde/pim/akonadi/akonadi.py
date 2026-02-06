# -*- coding: utf-8 -*-
import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "A storage service for PIM data and meta data"

        if CraftCore.compiler.isMacOS:
            # Hack to unblock build
            # It might an xcode issue because I couldn't reproduce locally anymore
            # after I updated xcode (or maybe that was placebo and it was something else)
            # Related to https://invent.kde.org/pim/akonadi/-/merge_requests/244
            self.patchToApply["25.08.3"] = [("macos-remove-assert.diff", 1)]

    def registerOptions(self):
        self.options.dynamic.registerOption("useDesignerPlugin", True)

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
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
        self.subinfo.options.configure.args += [
            "-DUSE_UNITY_CMAKE_SUPPORT=ON",
            "-DDATABASE_BACKEND=SQLITE",
            "-DAKONADI_RUN_MYSQL_ISOLATED_TESTS=OFF",
            f"-DBUILD_DESIGNERPLUGIN={self.subinfo.options.dynamic.useDesignerPlugin.asOnOff}",
        ]
