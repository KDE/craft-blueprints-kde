import info
from Package.AutoToolsPackageBase import *
from Package.MakeFilePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.1.32']:
            self.targets[ver] = 'ftp://xmlsoft.org/libxslt/libxslt-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'libxslt-' + ver
            if not CraftCore.compiler.isGCCLike():
                self.targetInstSrc[ver] = os.path.join(self.targetInstSrc[ver], 'win32')
        self.targetDigests['1.1.32'] = (['526ecd0abaf4a7789041622c3950c0e7f2c4c8835471515fd77eec684a355460'], CraftHash.HashAlgorithm.SHA256)

        self.description = "The GNOME XSLT C library and tools"
        self.defaultTarget = '1.1.32'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/libxml2"] = "default"
        self.runtimeDependencies["libs/zlib"] = "default"
        self.runtimeDependencies["libs/iconv"] = "default"


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
                            f"iconv=yes"]
                            )


class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared "
        
if CraftCore.compiler.isGCCLike():
    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)
else:
    class Package(PackageMSVC):
        def __init__(self):
            PackageMSVC.__init__(self)
