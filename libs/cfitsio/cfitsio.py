import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "library for the FITS (Flexible Image Transport System) file format"

        self.defaultTarget = '3.49'
        self.targets[self.defaultTarget] = 'http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-' + self.defaultTarget + '.tar.gz'
        self.targetInstSrc[self.defaultTarget] = "cfitsio-" + self.defaultTarget

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DENABLE_STATIC=ON"
