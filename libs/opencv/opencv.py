import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = 'a library for real time computer vision'

        # 4.1.2 and later are all on Github
        for ver in ['4.1.2', "4.2.0"]:
            self.targets[ver] = 'https://github.com/opencv/opencv/archive/' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'opencv-' + ver

        self.targetDigests['4.1.2'] = (['385dd0a9c25e67ef0dd60e022d2a2d7b17e2f36819cf3cb46aa8cdff5c5282c9'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['4.2.0'] = (['9ccb2192d7e8c03c58fee07051364d94ed7599363f3b0dce1c5e6cc11c1bb0ec'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '4.2.0'

        self.options.configure.args = "-DBUILD_NEW_PYTHON_SUPPORT=OFF -DBUILD_ZLIB=OFF -DBUILD_TIFF=OFF -DBUILD_JPEG=OFF -DBUILD_PNG=OFF -DBUILD_WEBP=OFF -DBUILD_JASPER=OFF -DWITH_JASPER=OFF -DBUILD_PROTOBUF=OFF -DPROTOBUF_UPDATE_FILES=ON -DWITH_QT=5"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/webp"] = None
        self.runtimeDependencies["libs/protobuf"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
