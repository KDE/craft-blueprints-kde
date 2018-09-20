import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/linuxdeploy/linuxdeploy.git"
        self.description = "AppDir creation and maintenance tool. Featuring flexible plugin system."
        self.webpage = "https://github.com/linuxdeploy/linuxdeploy"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True
        self.subinfo.options.configure.args += " -DUSE_SYSTEM_CIMG=OFF"

    def install(self):
        return utils.copyFile(os.path.join(self.buildDir(), "bin", "linuxdeploy"),
                              os.path.join(self.imageDir(), "bin", "linuxdeploy"))