import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = 'a library for real time computer vision'

        # 4.1.2 and later are all on Github
        for ver in ['4.1.2', '4.2.0', '4.3.0']:
            self.targets[ver] = 'https://github.com/opencv/opencv/archive/' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'opencv-' + ver
        self.patchToApply['4.3.0'] = [('opencv-pkgconfig-win-install.patch', 1)]

        self.targetDigests['4.1.2'] = (['385dd0a9c25e67ef0dd60e022d2a2d7b17e2f36819cf3cb46aa8cdff5c5282c9'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['4.2.0'] = (['9ccb2192d7e8c03c58fee07051364d94ed7599363f3b0dce1c5e6cc11c1bb0ec'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['4.3.0'] = (['68bc40cbf47fdb8ee73dfaf0d9c6494cd095cf6294d99de445ab64cf853d278a'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '4.3.0'

        self.options.configure.args = ' -DBUILD_LIST=tracking,face ' \
                + ' -DBUILD_ZLIB=OFF -DBUILD_TIFF=OFF -DBUILD_JPEG=OFF -DBUILD_WEBP=OFF -DBUILD_PROTOBUF=OFF -DBUILD_NEW_PYTHON_SUPPORT=OFF ' \
                + ' -DWITH_JASPER=OFF -DWITH_PNG=OFF -DWITH_OPENEXR=OFF -DWIH_VIDEOIO=OFF -DWITH_LAPACK=OFF -DWITH_V4L=OFF ' \
                + ' -DPROTOBUF_UPDATE_FILES=ON -DWITH_QT=5 ' \
                + ' -DOPENCV_GENERATE_PKGCONFIG=ON ' \
                + ' -DCPU_BASELINE=SSE2 -DCPU_DISPATCH=SSE2 -DOPENCV_ENABLE_ALLOCATOR_STATS=OFF ' \
                + ' -DOPENCV_INSTALL_BINARIES_PREFIX="" '
        # /!\ On openSuse, pkg-config is created in lib64/ instead of lib/

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/webp"] = None
        self.runtimeDependencies["libs/protobuf"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.contrib = CraftPackageObject.get('libs/opencv-contrib').instance
        self.subinfo.options.configure.args += ' -DOPENCV_EXTRA_MODULES_PATH="' \
            + OsUtils.toUnixPath(self.contrib.sourceDir()) + '/modules"'

    def fetch(self):
        return CMakePackageBase.fetch(self) and self.contrib.fetch(noop=False)

    def unpack(self):
        return CMakePackageBase.unpack(self) and self.contrib.unpack(noop=False)
