
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["5.41.0"] = [("0001-Also-look-for-qrencode-with-debug-suffix.patch", 1)]

        self.description = "Qt 5 addon providing a barcode api to produce QRCode barcodes and DataMatrix barcodes."

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qrencode"] = "default"
        self.runtimeDependencies["libs/libdmtx"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
