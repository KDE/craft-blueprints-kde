# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>

import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from Blueprints.CraftVersion import CraftVersion
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "Glaxnimate"
        self.description = "Simple vector animation program"
        self.webpage = "https://glaxnimate.mattbas.org/"

        for ver in ["0.5.4"]:
            self.targets[ver] = f"https://gitlab.com/mattbas/glaxnimate/-/archive/{ver}/glaxnimate-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"glaxnimate-{ver}"

        self.patchLevel["master"] = 1

        self.svnTargets["master"] = "https://invent.kde.org/graphics/glaxnimate.git"
        self.defaultTarget = "0.5.4"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        self.runtimeDependencies["libs/qt/qttools"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5" and CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/qt5/qtandroidextras"] = None
        self.runtimeDependencies["libs/potrace"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/libarchive"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/python"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        super().__init__()
        # enable submodule checkout
        self.subinfo.options.fetch.checkoutSubmodules = True
        self.subinfo.options.configure.args += [f"-DPython3_ROOT_DIR={CraftCore.standardDirs.craftRoot()}"]

    def createPackage(self):
        self.defines["executable"] = r"bin\glaxnimate.exe"
        self.addExecutableFilter(r"(bin|libexec)/(?!(glaxnimate|update-mime-database)).*")
        self.ignoredPackages.append("binary/mysql")
        # if not CraftCore.compiler.isLinux:
        #     self.ignoredPackages.append("libs/dbus")

        if self.buildTarget <= CraftVersion("0.5.4"):
            # this has been fixed in
            if CraftCore.compiler.isMacOS:
                self.defines["appname"] = "glaxnimate"
            else:
                self.defines["appname"] = "Glaxnimate"
        # self.defines["icon"] = os.path.join(self.sourceDir(), "data", "icons", "kdenlive.ico")
        # self.defines["icon_png"] = os.path.join(self.sourceDir(), "logo.png")
        return super().createPackage()
