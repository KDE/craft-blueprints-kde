import info


#
# this library is used by kdeedu/kstars
# the library is c-only
#
class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.13.0+svn270'] = 'download.sourceforge.net/kde-windows/libnova-0.13.0+svn270.tar.bz2'
        self.targetInstSrc['0.13.0+svn270'] = 'libnova'
        self.targetDigests['0.13.0+svn270'] = '1d618a5a1f4282e531b2a3d434407bac941cd700'
        self.patchToApply['0.13.0+svn270'] = [('libnova-20101215.diff', 1),
                                              ('libnova-20130629.diff', 1)]
        self.description = "a Celestial Mechanics, Astrometry and Astrodynamics library"
        self.defaultTarget = '0.13.0+svn270'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
