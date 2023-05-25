import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Simple DirectMedia Layer"
        self.webpage = "https://www.libsdl.org"
        for ver in ['2.0.9', '2.26.4']:
            self.targets[ver] = f"https://www.libsdl.org/release/SDL2-{ver}.tar.gz"
            self.targetInstSrc[ ver ] = f"SDL2-{ver}"
        self.patchToApply['2.0.9'] = [("libtool_windres.patch", 1)]
        self.targetDigests['2.0.9'] = (['255186dc676ecd0c1dbf10ec8a2cc5d6869b5079d8a38194c2aecdff54b324b1'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['2.26.4'] = (['1a0f686498fb768ad9f3f80b39037a7d006eac093aad39cb4ebcc832a8887231'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '2.26.4'

    def setDependencies(self):
        self.runtimeDependencies["libs/libsamplerate"] = None
        self.runtimeDependencies["libs/iconv"] = None


from Package.CMakePackageBase import *
from Package.AutoToolsPackageBase import *

if CraftCore.compiler.isAndroid:

    class Package(CMakePackageBase):
        def __init__(self, **args):
            CMakePackageBase.__init__(self)
else:

    # TODO: check if CMake works for other platforms too so we can replace AutoTools here
    class Package(AutoToolsPackageBase):
        def __init__(self, **args):
            AutoToolsPackageBase.__init__(self)
            self.subinfo.options.configure.autoreconf = False
            self.subinfo.options.configure.args = ["--disable-static", "--enable-threads", "--enable-directx", "--enable-libsamplerate"]
            if CraftCore.compiler.isFreeBSD:
                self.subinfo.options.configure.args += ["--disable-static", "--enable-threads", "--enable-directx", "--enable-libsamplerate"]
