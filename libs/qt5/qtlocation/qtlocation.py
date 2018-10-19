# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "The Qt Location API helps you create viable mapping solutions" \
                                " using the data available from some of the popular location services."
        self.tags = "Qt5Positioning, Qt5Location"

        # source: http://patchwork.ozlabs.org/patch/966318/
        # bug: https://bugreports.qt.io/browse/QTBUG-69512
        self.patchToApply["5.11.2"] = [("qt5location-fix-build-failure-due-to-GCC-5.x-bug-in-implicit-casts.diff", 1)]

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Package.Qt5CorePackageBase import *


class QtPackage(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage)
