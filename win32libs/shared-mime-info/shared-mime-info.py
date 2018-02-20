import shutil

import info
from Package.AutoToolsPackageBase import *



class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.9"]:
            self.targets[ver] = f"http://freedesktop.org/~hadess/shared-mime-info-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"shared-mime-info-{ver}"
        self.targetDigests["1.9"] = (['5c0133ec4e228e41bdf52f726d271a2d821499c2ab97afd3aa3d6cf43efcdc83'], CraftHash.HashAlgorithm.SHA256)

        self.description = "The shared-mime-info package contains the core database of common types and the update-mime-database command used to extend it"
        self.webpage = "https://www.freedesktop.org/wiki/Software/shared-mime-info/"
        self.defaultTarget = "1.9"

    def setDependencies(self):
        self.buildDependencies["dev-util/msys"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/gettext"] = "default"
        self.runtimeDependencies["win32libs/libxml2"] = "default"
        self.runtimeDependencies["win32libs/glib"] = "default"
        self.runtimeDependencies["win32libs/zlib"] = "default"
        if CraftCore.compiler.isMSVC():
            self.runtimeDependencies["kdesupport/kdewin"] = "default"


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        root = self.shell.toNativePath(CraftCore.standardDirs.craftRoot())
        self.subinfo.options.configure.args += f" --disable-default-make-check --disable-update-mimedb"
        self.subinfo.options.configure.cflags = f"-I{root}/include/glib-2.0 -I{root}/include/libxml2"
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.cflags += f" -I{root}/include/msvc"
            self.shell.useMSVCCompatEnv = True
            self.platform = ""
            self.subinfo.options.configure.args += f" PKG_CONFIG=':' "
            self.subinfo.options.configure.ldflags ="-lglib-2.0 -lgobject-2.0 -lgio-2.0 -lgthread-2.0 -llibxml2 -lintl -lzlib"
            if self.buildType() == "Debug":
                self.subinfo.options.configure.ldflags += " -lkdewind"
            else:
                self.subinfo.options.configure.ldflags += " -lkdewin"

