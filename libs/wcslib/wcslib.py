import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = 'World Coordinate System Library'
        for ver in ['7.7']:
            self.targets[ver] = 'http://indilib.org/jdownloads/wcslib/wcslib-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'wcslib-%s' % ver
        self.defaultTarget = '7.7'

    def setDependencies(self):
        self.runtimeDependencies["libs/cfitsio"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DENABLE_STATIC=ON"
