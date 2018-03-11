import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.2.0'] = "http://download.sourceforge.net/libwpg/libwpg-0.2.0.tar.bz2"
        self.targetInstSrc['0.2.0'] = "libwpg-0.2.0"
        self.patchToApply['0.2.0'] = ('libwpg-0.2.0-20110722.diff', 1)

        self.targetDigests['0.2.0'] = '34a692566bda66488f83c635774d1bd92cee0fdf'
        self.description = "A library to read and parse graphics in WPG (WordPerfect Graphics) format"
        self.defaultTarget = '0.2.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/libwpd"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
