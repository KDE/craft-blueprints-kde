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

        self.options.configure.args = (
                # build only modules needed by digikam & kdenlive
                ' -DBUILD_LIST=core,objdetect,imgproc,imgcodecs,dnn,flann,tracking'
                ' -DBUILD_EXAMPLES=OFF -DBUILD_TESTS=OFF -DBUILD_DOCS=OFF -DBUILD_PERF_TESTS=OFF'
                ' -DINSTALL_C_EXAMPLES=OFF -DINSTALL_PYTHON_EXAMPLES=OFF'
                # fix build failures (cmake failing tests in craft - linux or mingw)
                ' -DWITH_LAPACK=OFF -DWITH_V4L=OFF -DOPENCV_ENABLE_ALLOCATOR_STATS=OFF'
                # don't rebuild dependencies, use the ones we distribute
                ' -DOPENCV_BUILD_3RDPARTY_LIBS=OFF'
                ' -DBUILD_NEW_PYTHON_SUPPORT=OFF'
                ' -DBUILD_ZLIB=OFF -DBUILD_PROTOBUF=OFF'
                # disabled below ' -DBUILD_TIFF=OFF -DBUILD_JPEG=OFF -DBUILD_WEBP=OFF'
                # minimal dependencies (kdenlive)
                ' -DWITH_JASPER=OFF -DWITH_PNG=OFF -DWITH_OPENEXR=OFF'
                ' -DPROTOBUF_UPDATE_FILES=ON'
                # minimal dependencies (digikam)
                ' -DWITH_1394=OFF'
                ' -DWITH_CUBLAS=OFF -DWITH_CUDA=OFF -DWITH_CUFFT=OFF'
                ' -DWITH_DIRECTX=OFF -DWITH_DSHOW=OFF'
                ' -DWITH_EIGEN=OFF'
                ' -DWITH_FFMPEG=OFF -DWITH_GPHOTO2=OFF -DWITH_GSTREAMER=OFF -DWITH_GTK=OFF'
                ' -DWITH_IMGCODEC_HDR=OFF -DWITH_IMGCODEC_PXM=OFF -DWITH_IMGCODEC_SUNRASTER=OFF'
                ' -DWITH_IPP=OFF -DWITH_JPEG=OFF'
                ' -DWITH_MATLAB=OFF -DWITH_NVCUVID=OFF'
                ' -DWITH_OPENCL_SVM=OFF -DWITH_OPENCL=OFF -DWITH_OPENCLAMDBLAS=OFF -DWITH_OPENCLAMDFFT=OFF'
                ' -DWITH_OPENMP=OFF -DWITH_OPENNI=OFF'
                ' -DWITH_PVAPI=OFF'
                ' -DWITH_QT_OPENGL=OFF -DWITH_QT=OFF'
                ' -DWITH_QUICKTIME=OFF -DWITH_TBB=OFF -DWITH_TIFF=OFF -DWITH_UNICAP=OFF'
                ' -DWITH_VA_INTEL=OFF -DWITH_VFW=OFF -DWITH_VIDEOINPUT=OFF'
                ' -DWITH_VTK=OFF -DWITH_WEBP=OFF -DWITH_WIN32UI=OFF -DWITH_XINE=OFF'
                # MLT finds OpenCV through pkg-config
                ' -DOPENCV_GENERATE_PKGCONFIG=ON'
                # Avoid x64/mingw prefix on windows
                ' -DOPENCV_INSTALL_BINARIES_PREFIX=""'
                # Work on old machines
                ' -DCPU_BASELINE=SSE2 -DCPU_DISPATCH=SSE2'
                )

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/protobuf"] = None
        self.runtimeDependencies["libs/zlib"] = None
        # self.runtimeDependencies["libs/tiff"] = None
        # self.runtimeDependencies["libs/libjpeg-turbo"] = None
        # self.runtimeDependencies["libs/webp"] = None
        # self.runtimeDependencies["libs/ffmpeg"] = None
        # self.runtimeDependencies["libs/qt5/qtbase"] = None

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
