# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.33"]:
            self.targets[ver] = "http://dist.schmorp.de/libev/Attic/libev-" + ver + ".tar.gz"
            self.archiveNames[ver] = "libev-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "libev-" + ver
        self.description = "Asynchronous event library"
        self.defaultTarget = "4.33"
        self.patchToApply["4.33"] = ("libev-4.33.patch", 1)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        prefix = str(self.shell.toNativePath(CraftCore.standardDirs.craftRoot()))
        # self.subinfo.options.configure.bootstrap = True
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.configure.args += ["--disable-dependency-tracking", f"--prefix={prefix}"]
