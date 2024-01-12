import info
from CraftConfig import *
from Package.MesonPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "mpv"
        self.description = "Command line video player"
        self.svnTargets["master"] = "https://github.com/mpv-player/mpv.git"
        self.defaultTarget = "0.35.1"

        for ver in ["0.35.1"]:
            self.targets[ver] = f"https://github.com/mpv-player/mpv/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"mpv-{ver}"
            self.archiveNames[ver] = f"mpv-{ver}.tar.gz"

        self.targetDigests["0.35.1"] = (["41df981b7b84e33a2ef4478aaf81d6f4f5c8b9cd2c0d337ac142fc20b387d1a9"], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.buildDependencies["python-modules/meson"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/libass"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libarchive"] = None
        self.runtimeDependencies["libs/lcms2"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None

        if CraftCore.compiler.isLinux:
            self.runtimeDependencies["libs/libvdpau"] = None
            self.runtimeDependencies["libs/libva"] = None
            self.runtimeDependencies["libs/uuid"] = None

        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/lua"] = None


class Package(MesonPackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.args += ["-Drubberband=disabled", "-Dlibmpv=true"]

        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += ["-Dlua=disabled", "-Ddefault_library=static"]
        else:
            self.subinfo.options.configure.args += ["-Dlua=enabled"]
