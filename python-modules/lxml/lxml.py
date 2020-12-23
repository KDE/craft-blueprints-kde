# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = ''
        self.description = "Powerful and Pythonic XML processing library combining libxml2/libxslt with the ElementTree API."
        self.defaultTarget = 'master'


class Package(PipPackageBase):
    def __init__(self, **args):
        PipPackageBase.__init__(self)
