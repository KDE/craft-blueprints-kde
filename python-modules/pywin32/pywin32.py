# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):

    def setTargets(self):
        self.svnTargets['master'] = ''
        self.defaultTarget = 'master'


class WinPackage(PipPackageBase):
    def __init__(self, **args):
        PipPackageBase.__init__(self)
        self.python2 = False
        self.subinfo.options.package.disableBinaryCache = True

    def install(self):
        if not super().install():
            return False
        python = CraftCore.cache.findApplication("python")
        return utils.system(f"python {os.path.dirname(python)}/scripts/pywin32_postinstall.py -install")

from Package.MaybeVirtualPackageBase import *

class Package(MaybeVirtualPackageBase):
    def __init__(self):
        MaybeVirtualPackageBase.__init__(self, OsUtils.isWin(), classA=WinPackage)
