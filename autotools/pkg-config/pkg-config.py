# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.buildDependencies["dev-util/msys"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/glib"] = "default"

    def setTargets(self):
        self.description = "pkg-config is a helper tool used when compiling applications and libraries"
        self.svnTargets['master'] = 'git://anongit.freedesktop.org/pkg-config'
        for ver in ["0.26"]:
            self.targets[ver] = f"https://pkg-config.freedesktop.org/releases/pkg-config-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"pkg-config-{ver}"
        self.defaultTarget = '0.26'


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)

    def configure(self):
        root = self.shell.toNativePath(CraftCore.standardDirs.craftRoot())
        with utils.ScopedEnv({
            "GLIB_LIBS" : f"-L{os.path.join(root, 'lib')} -lglib-2.0",
            "GLIB_CFLAGS" : f"-I{os.path.join(root, 'include', 'glib-2.0')}"}):
            self.subinfo.options.configure.args += " --disable-static --enable-shared"
            return AutoToolsPackageBase.configure(self)

    def install(self):
        if not AutoToolsPackageBase.install(self):
            return False
        return self.copyToMsvcImportLib()
