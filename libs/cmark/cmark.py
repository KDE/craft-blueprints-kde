import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/commonmark/cmark'

        for ver in ['0.29.0']:
            self.targets[ver] = "https://github.com/commonmark/cmark/archive/%s.tar.gz" % ver
            self.archiveNames[ver] = 'cmark-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'cmark-%s' % ver

        self.defaultTarget = '0.29.0'
        self.description = "CommonMark parsing and rendering library and program in C"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += "-DCMARK_TESTS=OFF"
