# SPDX-FileCopyrightText: 2023 George Florea Bănuș <georgefb899@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause

import info
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "mpv"
        self.description = "Command line video player"
        self.svnTargets["master"] = "https://github.com/mpv-player/mpv.git"
        self.defaultTarget = "0.40.0"

        for ver in ["0.40.0", "0.39.0", "0.38.0"]:
            self.targets[ver] = f"https://github.com/mpv-player/mpv/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"mpv-{ver}"
            self.archiveNames[ver] = f"mpv-{ver}.tar.gz"

        self.targetDigests["0.40.0"] = (["10a0f4654f62140a6dd4d380dcf0bbdbdcf6e697556863dc499c296182f081a3"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.39.0"] = (["2ca92437affb62c2b559b4419ea4785c70d023590500e8a52e95ea3ab4554683"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.38.0"] = (["86d9ef40b6058732f67b46d0bbda24a074fae860b3eaae05bab3145041303066"], CraftHash.HashAlgorithm.SHA256)

        # force rebuild after libplacebo ABI break
        self.patchLevel["0.39.0"] = 1

    def setDependencies(self):
        self.buildDependencies["python-modules/meson"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/libass"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/lcms2"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/libplacebo"] = None

        if CraftCore.compiler.isLinux:
            self.runtimeDependencies["libs/libvdpau"] = None
            self.runtimeDependencies["libs/libva"] = None
            self.runtimeDependencies["libs/uuid"] = None

        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/lua"] = None
            self.runtimeDependencies["libs/libarchive"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-Drubberband=disabled", "-Dlibmpv=true"]

        if CraftCore.compiler.isAndroid:
            # Using libarchive causes linker errors on Android, but we don't need it right now
            self.subinfo.options.configure.args += ["-Dlua=disabled", "-Ddefault_library=static", "-Dlibarchive=disabled", "-Dcplayer=false"]
        else:
            self.subinfo.options.configure.args += ["-Dlua=enabled"]
