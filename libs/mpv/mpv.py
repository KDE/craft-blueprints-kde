import info
from CraftConfig import *
from Package.MesonPackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "mpv"
        self.description = "Command line video player"
        self.svnTargets["e6c5d58"] = "https://github.com/mpv-player/mpv.git||e6c5d58d1ed95c503ec7261a3d85de32315192cf"
        self.defaultTarget = "e6c5d58"

    def setDependencies( self ):
        self.buildDependencies["python-modules/meson"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/lua"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/libass"] = None
        self.runtimeDependencies["libs/uuid"] = None
        self.runtimeDependencies["libs/libva"] = None
        self.runtimeDependencies["libs/libvdpau"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libarchive"] = None
        self.runtimeDependencies["libs/lcms2"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/rubberband"] = None

class Package(MesonPackageBase):
    def __init__(self, **args):
        MesonPackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-Drubberband=disabled", "-Dlua=enabled", "-Dlibmpv=true"]
