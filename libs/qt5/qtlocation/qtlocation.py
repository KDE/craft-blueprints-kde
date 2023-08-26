# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.registerOption("enableProprietaryPlugins", False)

    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = (
            "The Qt Location API helps you create viable mapping solutions" " using the data available from some of the popular location services."
        )
        self.tags = "Qt5Positioning, Qt5Location"

        # source: http://patchwork.ozlabs.org/patch/966318/
        # bug: https://bugreports.qt.io/browse/QTBUG-69512
        self.patchToApply["5.11.2"] = [("qt5location-fix-build-failure-due-to-GCC-5.x-bug-in-implicit-casts.diff", 1)]
        self.patchToApply["5.12.0"] = [("qt5location-fix-build-failure-due-to-GCC-5.x-bug-in-implicit-casts.diff", 1)]
        if CraftCore.compiler.isFreeBSD:
            self.patchToApply["5.15.2"] = [("freebsd-compat.diff", 1)]

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None


from Package.Qt5CorePackageBase import *


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)
        if not self.subinfo.options.dynamic.enableProprietaryPlugins:
            self.subinfo.options.dynamic.featureArguments += [
                "-no-feature-geoservices_esri",
                "-no-feature-geoservices_mapbox",
                "-no-feature-geoservices_mapboxgl",
                "-no-feature-geoservices_here",
            ]
