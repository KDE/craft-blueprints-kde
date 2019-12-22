import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.defaultTarget = '4.1.2'
        self.description = 'a library for real time computer vision'

        # 4.1.2 and later are all on Github
        for ver in ['4.1.2']:
            self.targets[ver] = 'https://github.com/opencv/opencv/archive/' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'opencv-' + ver

        self.targetDigests['4.1.2'] = '385dd0a9c25e67ef0dd60e022d2a2d7b17e2f36819cf3cb46aa8cdff5c5282c9'

        self.options.configure.args = "-DBUILD_NEW_PYTHON_SUPPORT=OFF"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.make.supportsMultijob = False
