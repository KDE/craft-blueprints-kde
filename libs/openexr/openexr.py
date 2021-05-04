import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.5.5"]:
            self.targets[ver] = 'https://github.com/AcademySoftwareFoundation/openexr/archive/refs/tags/v' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'libpng-' + ver

        self.description = 'The OpenEXR project provides the specification and reference implementation of the EXR file format, the professional-grade image storage format of the motion picture industry.'
        self.defaultTarget = '2.5.5'

    def setDependencies(self):
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
