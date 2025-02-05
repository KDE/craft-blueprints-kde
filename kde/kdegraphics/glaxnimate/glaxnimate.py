# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <julius.kuenzel@kde.org>

import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from Packager.AppImagePackager import AppImagePackager


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "Glaxnimate"
        self.description = "Simple vector animation program"
        self.webpage = "https://glaxnimate.mattbas.org/"

        for ver in ["0.5.80"]:
            self.targets[ver] = f"https://download.kde.org/unstable/glaxnimate/{ver}/glaxnimate-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/unstable/glaxnimate/{ver}/glaxnimate-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"glaxnimate-{ver}"

        self.svnTargets["master"] = "https://invent.kde.org/graphics/glaxnimate.git"
        self.patchLevel["master"] = 1

        self.defaultTarget = "0.5.80"

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
        # QtTools is indeed a runtim dep for the plugin system
        self.runtimeDependencies["libs/qt/qttools"] = None
        self.runtimeDependencies["libs/potrace"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/libarchive"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None
        self.runtimeDependencies["libs/python"] = None
        if not CraftCore.compiler.isAndroid:  # and not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["python-modules/lottie"] = None
            self.runtimeDependencies["python-modules/pillow"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # enable submodule checkout
        self.subinfo.options.fetch.checkoutSubmodules = True
        self.subinfo.options.configure.args += [f"-DPython3_ROOT_DIR={CraftCore.standardDirs.craftRoot()}"]

    def setDefaults(self, defines: {str: str}) -> {str: str}:
        defines = super().setDefaults(defines)
        if CraftCore.compiler.isLinux and isinstance(self, AppImagePackager):
            defines["runenv"] += [
                "PYTHONHOME=$this_dir/usr",
            ]
        return defines

    def createPackage(self):
        self.defines["executable"] = r"bin\glaxnimate.exe"
        self.addExecutableFilter(r"(bin|libexec)/(?!(glaxnimate|update-mime-database)).*")
        self.ignoredPackages.append("binary/mysql")
        # llvm is pulled in by QtTools
        self.ignoredPackages.append("libs/llvm")
        # if not CraftCore.compiler.isLinux:
        #     self.ignoredPackages.append("libs/dbus")

        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(self.blueprintDir() / "exclude_macos.list")

        # For the Microsoft Store
        # We need to change this, because for unknown reasons the store does not
        # assign the usual KDEe.V.Glaxnimate as for other apps
        self.defines["appx_identity_name"] = "KDEe.V.47488D4059B84"

        self.defines["icon"] = self.sourceDir() / "data/images/glaxnimate.ico"
        self.defines["icon_png"] = self.sourceDir() / "data/images/glaxnimate.png"

        return super().createPackage()
