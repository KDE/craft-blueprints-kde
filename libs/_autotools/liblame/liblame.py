# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['3.100']:
            self.targets[ver] = f'https://sourceforge.net/projects/lame/files/lame/{ver}/lame-{ver}.tar.gz'
            
            self.targetInstSrc[ver] = 'lame-'+ver
        self.patchToApply['3.100'] = [("lame_init_old-missing-symfile.patch", 1)]
        self.targetDigests['3.100'] = (['ddfe36cab873794038ae2c1210557ad34857a4b6bdc515785d1da9e175b1da1e'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '3.100'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/msys"] = None
        self.buildDependencies["dev-utils/nasm"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.configure.args = " --disable-static --disable-gtktest --disable-frontend --enable-nasm "
