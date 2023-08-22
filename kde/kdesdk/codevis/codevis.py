import subprocess
import sys

from Blueprints.CraftVersion import CraftVersion
import info
from info import DependencyRequirementType

class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Codevis is a software to visualize large software architectures."
        self.displayName = "Codevis"
        self.webpage = "http://invent.kde.org/sdk/codevis"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/llvm"] = None
        self.runtimeDependencies["libs/catch2"] = None
        self.runtimeDependencies["libs/runtime"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtwebengine"] = (None, DependencyRequirementType.Required)

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.defines["executable"] = "bin\\codevis.exe"

        return TypePackager.createPackage(self)
