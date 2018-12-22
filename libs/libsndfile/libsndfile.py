import info

from Package.CMakePackageBase import *
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.0.24', '1.0.28']:
            self.targets[ver] = 'http://www.mega-nerd.com/libsndfile/files/libsndfile-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'libsndfile-' + ver
            if not CraftCore.compiler.isGCCLike():
                self.patchToApply[ver] = [('libsndfile-1.0.24-20131003.diff', 1)]
        self.targetDigests['1.0.24'] = 'ade2dad272b52f61bb58aca3a4004b28549ee0f8'
        self.targetDigests['1.0.28'] = (['1ff33929f042fa333aed1e8923aa628c3ee9e1eb85512686c55092d1e5a9dfa9'], CraftHash.HashAlgorithm.SHA256)

        self.description = "a C library for reading and writing files containing sampled sound"
        self.defaultTarget = '1.0.28'

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libogg"] = None
        self.runtimeDependencies["libs/libvorbis"] = None


if CraftCore.compiler.isGCCLike():
    class Package(AutoToolsPackageBase):
        def __init__(self):
            AutoToolsPackageBase.__init__(self)
else:
    class Package(CMakePackageBase):
        def __init__(self):
            CMakePackageBase.__init__(self)

