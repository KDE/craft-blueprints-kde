# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Akonadi Search Agent"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/xapian-core"] = None
        self.runtimeDependencies["kde/pim/akonadi"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/pim/akonadi-mime"] = None
        self.runtimeDependencies["kde/pim/kmime"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcalendarcore"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcontacts"] = None
        self.runtimeDependencies["kde/libs/ktextaddons"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DUSE_UNITY_CMAKE_SUPPORT=ON"]
