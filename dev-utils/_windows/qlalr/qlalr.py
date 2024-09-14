import os

import info
from Package.BinaryPackageBase import BinaryPackageBase

# sources are in qt.git/util/qlalr, binary is here.
# To build qlalr yourself, go into the Qt sources,
# cd into util/qlalr, and run the following command:
# qmake && nmake
# Additionally, the binary is packaged with upx
# This binary is from the 4.7.0 version of Qt


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["HEAD"] = "http://www.winkde.org/pub/kde/ports/win32/repository/other/qlalr.exe"
        self.defaultTarget = "HEAD"
        self.targetInstallPath["HEAD"] = os.path.join("dev-utils", "bin")


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
