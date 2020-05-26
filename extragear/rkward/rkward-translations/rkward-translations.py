import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://invent.kde.org/tfry/rkward-po-export.git'
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

from Package.VirtualPackageBase import *


class Package(SourceComponentPackageBase):
    def __init__(self):
        SourceComponentPackageBase.__init__(self)


