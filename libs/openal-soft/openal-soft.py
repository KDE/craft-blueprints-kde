import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.19.1']:
            self.targets[ver] = \
                f'https://github.com/kcat/openal-soft/archive/openal-soft-{ver}.tar.gz'
            self.targetInstSrc[ver] = f'openal-soft-openal-soft-{ver}'
        self.targetDigests["1.19.1"] = (['9f3536ab2bb7781dbafabc6a61e0b34b17edd16bd6c2eaf2ae71bc63078f98c7'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.19.1"] = [("openal-soft-1.19.1-20191017.diff", 1),  ("openal-soft-1.19.1-20191019.diff", 1)]
        self.description = 'a library for audio support'
        self.defaultTarget = '1.19.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/qt5/qtbase"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-DALSOFT_EXAMPLES=OFF"]
        # fix dsound.h search
        # TODO: fix the find script ...
        if CraftCore.compiler.isMinGW():
            if CraftCore.compiler.isX64():
                self.subinfo.options.configure.args += [f"-DCMAKE_SYSTEM_PREFIX_PATH={CraftCore.standardDirs.craftRoot()}/mingw64/x86_64-w64-mingw32"]
            else:
                self.subinfo.options.configure.args += [f"-DCMAKE_SYSTEM_PREFIX_PATH={CraftCore.standardDirs.craftRoot()}/mingw/i686-w64-mingw32"]
