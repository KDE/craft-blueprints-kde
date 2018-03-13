import info
from Package.CMakePackageBase import *


##########################################################################
############################# ATTENTION ##################################
##########################################################################
######### There is no binary build for Windows Ce, just the lib! #########
##########################################################################

class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['1.0.6'] = 'http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz'
        self.targetInstSrc['1.0.6'] = "bzip2-1.0.6"
        self.patchToApply['1.0.6'] = ("bzip.diff", 1)
        self.targetDigests['1.0.6'] = '3f89f861209ce81a6bab1fd1998c0ef311712002'
        self.description = "shared libraries for handling bzip2 archives (runtime)"
        self.defaultTarget = '1.0.6'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.supportsNinja = False
        self.subinfo.options.package.packageName = 'libbzip2'
        # self.supportsNinja = False
