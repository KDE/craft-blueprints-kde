import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Simple DirectMedia Layer"
        self.webpage = "https://www.libsdl.org"
        for ver in ['2.0.8']:
            self.targets[ver] = f"https://www.libsdl.org/release/SDL2-{ver}.tar.gz"
            self.targetInstSrc[ ver ] = f"SDL2-{ver}"
        self.targetDigests['2.0.8'] = (['edc77c57308661d576e843344d8638e025a7818bff73f8fbfab09c3c5fd092ec'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '2.0.8'

    def setDependencies(self):
        self.runtimeDependencies["libs/libsamplerate"] = None
        self.runtimeDependencies["libs/iconv"] = None

from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = "--enable-threads --enable-directx --enable-libsamplerate"
