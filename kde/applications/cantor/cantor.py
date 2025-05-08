# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Stefan Gerlach <stefan.gerlach@uni.kn>

import info
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Packager.AppxPackager import AppxPackager


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Cantor"
        self.patchToApply["24.12.3"] = [("cantor-24.12.2-qt5compat.patch", 1)]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtwebengine"] = None
        self.runtimeDependencies["libs/qt/qttools"] = None
        self.runtimeDependencies["qt-libs/poppler"] = None
        self.runtimeDependencies["libs/python"] = None
        # using included discount
        # self.runtimeDependencies["libs/discount"] = None
        # required on macOS
        if CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/expat"] = None
            self.runtimeDependencies["libs/webp"] = None
        if CraftCore.compiler.isWindows:
            self.runtimeDependencies["binary/r-base"] = None
        else:
            self.runtimeDependencies["libs/r-base"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kpty"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/applications/analitza"] = None
        # ld: unknown options: -soname (gcc vs. clang?)
        # self.runtimeDependencies["libs/lua"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # if CraftCore.compiler.isWindows:
        # self.subinfo.options.make.supportsMultijob = False

        # R backend fail compiling on Windows
        # self.r_dir = os.path.join(CraftCore.standardDirs.craftRoot(), "lib", "R", "bin", "x64")
        # self.subinfo.options.configure.args += [f"-DR_EXECUTABLE={OsUtils.toUnixPath(os.path.join(self.r_dir, "R.exe"))}"]
        # self.subinfo.options.configure.args += [f"-DR_R_LIBRARY={OsUtils.toUnixPath(os.path.join(self.r_dir, "R.dll"))}"]

        # pythonPath = CraftCore.settings.get("Paths", "PYTHON")
        self.subinfo.options.configure.args += [f"-DPython3_ROOT_DIR={CraftCore.standardDirs.craftRoot()}"]

        # old method
        # if CraftCore.compiler.isMSVC():
        #    self.subinfo.options.configure.args += [
        #        f"-DPython3_EXECUTABLE:FILEPATH={OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/bin/python.exe",
        #        f"-DPython3_LIBRARY:FILEPATH={OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/lib/python311.lib",
        #        f"-DPython3_INCLUDE_DIR:FILEPATH={OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/include/python3.11",
        #        "-DPython3_FIND_REGISTRY=NEVER",
        #    ]

        # help thirdparty discount on macOS.x86_64
        if CraftCore.compiler.isMacOS and CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
            self.subinfo.options.configure.cflags += "-arch x86_64"

    def createPackage(self):
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        # Some plugins files break code signing on macOS, which is picky about file names
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(self.blueprintDir() / "blacklist_mac.txt")

        self.ignoredPackages.append("binary/mysql")
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")

        self.defines["appname"] = "cantor"
        self.defines["website"] = "https://cantor.kde.org/"
        self.defines["executable"] = "bin\\cantor.exe"
        self.defines["shortcuts"] = [{"name": "Cantor", "target": "bin/cantor.exe", "description": self.subinfo.description, "icon": "$INSTDIR\\cantor.ico"}]
        self.defines["icon"] = self.blueprintDir() / "cantor.ico"
        if self.buildTarget == "master":
            self.defines["icon_png"] = self.sourceDir() / "icons/150-apps-cantor.png"
            self.defines["icon_png_44"] = self.sourceDir() / "icons/44-apps-cantor.png"
            self.defines["icon_png_310"] = self.sourceDir() / "icons/310-apps-cantor.png"

        if isinstance(self, AppxPackager):
            self.defines["display_name"] = "Cantor"

        # see labplot.py for more

        return super().createPackage()
