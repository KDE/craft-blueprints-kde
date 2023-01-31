import glob
from xml.etree import ElementTree as et

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['2.0.0'] = "https://github.com/indilib/indi.git|v2.0.0"
        self.defaultTarget = '2.0.0'
        self.description = 'INDI Library'

    def setDependencies(self):
        self.buildDependencies["dev-utils/grep"] = None
        self.buildDependencies["libs/zlib"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/libnova"] = None
        self.runtimeDependencies["libs/cfitsio"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DINDI_BUILD_SERVER=OFF -DINDI_BUILD_DRIVERS=OFF -DINDI_BUILD_CLIENT=ON -DINDI_BUILD_QT5_CLIENT=OFF -DINDI_BUILD_SHARED=OFF"
