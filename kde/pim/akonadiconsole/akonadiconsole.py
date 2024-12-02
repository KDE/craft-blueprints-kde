# -*- coding: utf-8 -*-
import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Akonadi Console Tools"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcontacts"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcalendarcore"] = None
        self.runtimeDependencies["kde/pim/kpimtextedit"] = None
        self.runtimeDependencies["kde/pim/akonadi"] = None
        self.runtimeDependencies["kde/pim/akonadi-mime"] = None
        self.runtimeDependencies["kde/pim/libkdepim"] = None
        self.runtimeDependencies["kde/pim/kmime"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None

        if not CraftCore.compiler.isWindows:
            self.runtimeDependencies["kde/pim/akonadi-contacts"] = None
            self.runtimeDependencies["kde/pim/calendarsupport"] = None
            self.runtimeDependencies["kde/pim/messagelib"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DUSE_UNITY_CMAKE_SUPPORT=ON"]
        self.subinfo.options.dynamic.buildTests = False
        if not self.subinfo.options.isActive("binary/mysql"):
            self.subinfo.options.configure.args += ["-DDATABASE_BACKEND=SQLITE"]

    def createPackage(self):
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        self.defines["shortcuts"] = [{"name": "AkonadiConsole", "target": "bin/akonadiconsole.exe", "description": self.subinfo.description}]
        self.defines["icon_png"] = self.blueprintDir() / "150-apps-akonadiconsole.png"
        self.defines["icon_png_44"] = self.blueprintDir() / "44-apps-akonadiconsole.png"
        self.defines["alias"] = "akonadiconsole"
        return super().createPackage()
