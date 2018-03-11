import info

from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.0.14', '1.0.16']:
            self.targets[ver] = 'http://download.librdf.org/source/redland-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'redland-' + ver
        self.patchToApply['1.0.14'] = [('redland-1.0.14-20130523.diff', 1)]
        self.targetDigests['1.0.14'] = '2561bf73f00f88e39f5c7b3a9b78f8d4ce7da955'
        self.patchToApply['1.0.16'] = [('redland-1.0.16-20130901.diff', 1)]
        self.targetDigests['1.0.16'] = '0dc3d65bee6d580cae84ed261720b5b4e6b1f856'

        self.description = "Resource Description Framework (RDF)"
        self.defaultTarget = '1.0.16'

    def setDependencies(self):
        self.runtimeDependencies["libs/raptor2"] = "default"
        self.runtimeDependencies["libs/rasqal"] = "default"
        self.runtimeDependencies["libs/sqlite"] = "default"
        self.runtimeDependencies["libs/pthreads"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
