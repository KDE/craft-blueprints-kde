import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.1.26"]:
            self.targets[ver] = "ftp://ftp.cyrusimap.org/cyrus-sasl/cyrus-sasl-" + ver + ".tar.gz"
            self.targetInstSrc[ver] = "cyrus-sasl-" + ver
            #http://www.linuxfromscratch.org/blfs/view/svn/postlfs/cyrus-sasl.html
            self.patchToApply["2.1.26"] = [("cyrus-sasl-2.1.26-fixes-3.patch", 1),
                                           ("cyrus-sasl-2.1.26-openssl-1.1.0-1.patch", 1)]
        if CraftCore.compiler.isWindows:
            self.patchToApply["2.1.26"] += [("cyrus-sasl-2.1.26.patch", 1)]
        self.targetDigests["2.1.26"] = "d6669fb91434192529bd13ee95737a8a5040241c"
        self.patchLevel["2.1.26"] = 1
        self.description = "Cyrus SASL implementation"
        self.defaultTarget = "2.1.26"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class CMakePackage(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -DSTATIC_LIBRARY=OFF"


from Package.AutoToolsPackageBase import *

class PackageAutotools(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.bootstrap = True
        self.subinfo.options.configure.args += " --disable-macos-framework"

if CraftCore.compiler.isWindows:
    class Package(CMakePackage):
        pass
else:
    class Package(PackageAutotools):
        pass
