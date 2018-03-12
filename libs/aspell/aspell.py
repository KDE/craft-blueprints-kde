import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['0.60.6', '0.60.6.1']:
            self.targets[ver] = 'ftp://ftp.gnu.org/gnu/aspell/aspell-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'aspell-%s' % ver
        self.targetDigests['0.60.6'] = '335bcb560e00f59d89ec9e4c4114c325fb0e65f4'
        self.targetDigests['0.60.6.1'] = 'ff1190db8de279f950c242c6f4c5d5cdc2cbdc49'

        self.patchToApply['0.60.6'] = [('aspell-0.60.6-20100726.diff', 1)]
        self.patchToApply['0.60.6.1'] = [('aspell-0.60.6-20100726.diff', 1)]
        self.description = "A powerful spell checker, designed to replace ispell"
        self.defaultTarget = '0.60.6.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-utils/perl"] = "default"
        self.runtimeDependencies["libs/win_iconv"] = "default"
        self.runtimeDependencies["data/aspell-data"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
