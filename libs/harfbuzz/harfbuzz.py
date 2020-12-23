import info

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.7.2"]:
            self.targets[ver] = f"https://github.com/harfbuzz/harfbuzz/archive/{ver}.tar.gz"
            self.targetInstSrc[ ver ] = "harfbuzz-" + ver
        self.targetDigests['2.7.2'] = (['8ec112ee108642477478b75fc7906422abed404d7530e47ba0a4875f553f1b59'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["2.7.2"] = [("cmake-generate-pkgconfig.patch", 0)]
        self.description = "Text shaping library"
        self.defaultTarget = '2.7.2'

    def setDependencies(self):
        self.runtimeDependencies["libs/freetype"] = None
        self.runtimeDependencies["libs/glib"] = None
        self.buildDependencies["libs/icu"] = None
        self.buildDependencies["libs/cairo"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += ' -DBUILD_SHARED_LIBS=ON '
