# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.buildDependencies["libs/boost/boost-headers"] = "default"

    def setTargets(self):
        self.svnTargets['master_KDE'] = 'git://anongit.kde.org/libechonest'
        self.svnTargets['master'] = '[git]https://github.com/lfranchi/libechonest.git'
        self.targetSrcSuffix['master'] = "-github"

        for ver in ['1.2.1', '2.0.1', '2.0.2', '2.0.3', '2.3.1']:
            self.targets[ver] = 'http://files.lfranchi.com/libechonest-%s.tar.bz2' % ver
            self.targetInstSrc[ver] = 'libechonest-%s' % ver
        self.targetDigests['1.2.1'] = '5ad5897c91c365b32840e75e806c9725c89b4522'
        self.targetDigests['2.0.1'] = '5dd98ffb370e0e199e37ece4a1775a05594f3dcb'
        self.targetDigests['2.0.2'] = '346eba6037ff544f84505941832604668c1e5b2b'
        self.targetDigests['2.0.3'] = '10ada8aced6dce3c0d206afcfbd4b05313bd4d04'
        self.targetDigests['2.3.1'] = '9d7245c71e707651a7054ce6f0d90b9a62004b23'
        self.patchToApply['2.0.3'] = ('libechonest-2.0.3-20130419.diff', 1)
        self.defaultTarget = '2.3.1'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DBUILD_WITH_QT4=OFF "
