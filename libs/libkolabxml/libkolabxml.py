# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['0.8.2', '0.8.4', '1.0.1']:
            self.targets[ver] = 'http://git.kolab.org/libkolabxml/snapshot/libkolabxml-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = "libkolabxml-" + ver
        self.patchToApply['0.8.2'] = [("libkolabxml-fixes.diff", 1)]
        self.patchToApply['0.8.4'] = [("libkolabxml-fixes.diff", 1)]
        self.patchToApply['1.0.1'] = [("libkolabxml-1.0.1-fixes.diff", 1)]

        self.description = 'Kolab XML Format Schema Definitions Library'
        self.defaultTarget = '1.0.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies['dev-util/xsd'] = 'default'
        self.buildDependencies["libs/xerces-c"] = "default"

        # the following runtimeDependencies are runtime runtimeDependencies for packages linking to the static! libkolabxml
        self.runtimeDependencies["libs/boost/boost-thread"] = "default"
        self.runtimeDependencies["libs/boost/boost-system"] = "default"
        self.runtimeDependencies["libs/libcurl"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DBUILD_TESTS=OFF"
