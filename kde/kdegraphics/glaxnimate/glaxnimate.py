# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>

import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
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
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        self.runtimeDependencies["libs/qt/qttools"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5" and CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/qt5/qtandroidextras"] = None
        self.runtimeDependencies["libs/potrace"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/libarchive"] = None
        self.runtimeDependencies["libs/zlib"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        super().__init__()
        # enable submodule checkout
        self.subinfo.options.fetch.checkoutSubmodules = True

    def make(self):
        args = self.makeOptions("translations")
        return super().make() and utils.system([self.makeProgram, args])

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isLinux:
            utils.copyFile(self.buildDir() / "external/Qt-Color-Widgets/libQtColorWidgets.so.2.2.0", self.installDir() / "lib/libQtColorWidgets.so.2.2.0")
            utils.copyFile(self.buildDir() / "external/Qt-Color-Widgets/libQtColorWidgets.so.2", self.installDir() / "lib/libQtColorWidgets.so.2")
            utils.copyFile(self.buildDir() / "external/Qt-Color-Widgets/libQtColorWidgets.so", self.installDir() / "lib/libQtColorWidgets.so")
        if CraftCore.compiler.isAndroid:
            utils.copyFile(
                self.buildDir() / "android-build/libs" / CraftCore.compiler.androidAbi / f"libQtColorWidgets_{CraftCore.compiler.androidAbi}.so",
                self.installDir() / f"lib/libQtColorWidgets_{CraftCore.compiler.androidAbi}.so",
            )
        if CraftCore.compiler.isWindows:
            utils.copyFile(self.buildDir() / "external/Qt-Color-Widgets/libQtColorWidgets.dll", self.installDir() / "bin/libQtColorWidgets.dll")
        return True

    def createPackage(self):
        self.defines["executable"] = r"bin\glaxnimate.exe"
        # self.addExecutableFilter(r"(bin|libexec)/(?!(glaxnimate|update-mime-database)).*")
        self.ignoredPackages.append("binary/mysql")
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")

        self.defines["appname"] = "Glaxnimate"
        # self.defines["icon"] = os.path.join(self.sourceDir(), "data", "icons", "kdenlive.ico")
        # self.defines["icon_png"] = os.path.join(self.sourceDir(), "logo.png")
        return super().createPackage()
