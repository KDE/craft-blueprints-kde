import info
from Package.AutoToolsPackageBase import *
from Package.MakeFilePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['2.9.7']:
            self.targets[ver] = 'ftp://xmlsoft.org/libxml2/libxml2-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'libxml2-' + ver
            if not CraftCore.compiler.isGCCLike():
                self.targetInstSrc[ver] = os.path.join(self.targetInstSrc[ver], 'win32')
        self.targetDigests['2.9.7'] = (['f63c5e7d30362ed28b38bfa1ac6313f9a80230720b7fb6c80575eeab3ff5900c'], CraftHash.HashAlgorithm.SHA256)
        self.description = "XML C parser and toolkit (runtime and applications)"
        self.defaultTarget = '2.9.7'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/zlib"] = "default"
        self.runtimeDependencies["win32libs/win_iconv"] = "default"
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"


class PackageMSVC(MakeFilePackageBase):
    def __init__(self, **args):
        MakeFilePackageBase.__init__(self)
        self.supportsNinja = False
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.make.supportsMultijob = False

    def configure(self):
        self.enterSourceDir()
        includedir = os.path.join(CraftCore.standardDirs.craftRoot(), 'include')
        libdir = os.path.join(CraftCore.standardDirs.craftRoot(), 'lib')
        prefixdir = self.imageDir()
        builddebug = "yes" if self.buildType() == "Debug" else "no"

        return utils.system([f"cscript.exe",
                            f".\configure.js",
                            f"compiler=msvc",
                            f"include={includedir}",
                            f"lib={libdir}",
                            f"prefix={prefixdir}",
                            f"debug={builddebug}",
                            f"zlib=yes",
                            f"iconv=yes"])

    def install(self):
        if not MakeFilePackageBase.install(self):
            return False
        includedir = os.path.join(self.imageDir(), "include")
        libxmldir = os.path.join(includedir, "libxml2")
        utils.moveDir(os.path.join(libxmldir, "libxml"), includedir) #otherwise it isn't picked up by libxslt
        return True


class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared --without-python "

if CraftCore.compiler.isGCCLike():
    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)
else:
    class Package(PackageMSVC):
        def __init__(self):
            PackageMSVC.__init__(self)
