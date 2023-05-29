import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['0.9.7']:
            # self.targets[ver] = 'https://github.com/jrfonseca/drmingw/archive/' + ver + '.tar.gz'
            # self.targetInstSrc[ver] = 'drmingw-' + ver
            # We need to use git instead of the tars, becuase at the moment
            # the tars to not contain the git submodule that are required
            self.svnTargets[ver] = 'https://github.com/jrfonseca/drmingw.git||' + ver
        self.targetDigests['0.9.7'] = (['79f62ab2411b54021c71af7ed6c92487ec0019af61ecfe62a2466048402ec81e'], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets['master'] = "https://github.com/jrfonseca/drmingw.git"

        self.description = "Postmortem debugging tools for MinGW."
        self.defaultTarget = '0.9.7'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True
        self.subinfo.options.configure.args = " -DPOSIX_THREADS=ON "
