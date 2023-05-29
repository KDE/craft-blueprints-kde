import glob
from xml.etree import ElementTree as et

import info


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "0.2.2"
        self.targets[ver] = "https://gitea.nouspiro.space/nou/libXISF/archive/v%s.tar.gz" % ver
        self.svnTargets["master"] = "https://gitea.nouspiro.space/nou/libXISF"
        self.targetInstSrc[ver] = "libxisf"
        self.defaultTarget = ver
        self.description = "XISF Library"

    def setDependencies(self):
        self.buildDependencies["libs/zlib"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DBUILD_SHARED_LIBS=OFF -DUSE_BUNDLED_LZ4=ON -DUSE_BUNDLED_PUGIXML=ON -DUSE_BUNDLED_ZLIB=OFF"
