# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/digikam.git'

        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies['libs/x265'] = 'default'
        self.runtimeDependencies['libs/tiff'] = 'default'
        self.runtimeDependencies['libs/boost'] = 'default'
        self.runtimeDependencies['libs/expat'] = 'default'
        self.runtimeDependencies['libs/ffmpeg'] = 'default'
        self.runtimeDependencies['libs/lcms2'] = 'default'
        self.runtimeDependencies['libs/eigen3'] = 'default'
        self.runtimeDependencies['libs/exiv2'] = 'default'
        self.runtimeDependencies['libs/opencv'] = 'default'
        self.runtimeDependencies['libs/lensfun'] = 'default'
        self.runtimeDependencies['libs/libpng'] = 'default'
        self.runtimeDependencies['libs/libjpeg-turbo'] = 'default'

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
