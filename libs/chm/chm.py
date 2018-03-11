import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.40'] = 'http://www.jedrea.com/chmlib/chmlib-0.40.tar.bz2'
        self.patchToApply['0.40'] = ('chm-cmake.diff', 0)
        self.targetInstSrc['0.40'] = 'chmlib-0.40'
        self.targetDigests['0.40'] = '5231d7531e8808420d7f89fd1e4fdbac1ed7a167'
        self.description = "a library for dealing with Microsoft ITSS/CHM format files"
        self.defaultTarget = '0.40'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        # building examples and debugging tools
        self.subinfo.options.configure.args = "-DBUILD_examples=OFF"
