import info


class subinfo(info.infoclass):
    def setTargets(self):
        # not used  yet only for reference
        self.targets['master'] = ""
        self.description = "The d3dcompiler*.dll for qml"
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-util/mingw-w64"] = "default"


from Package.BinaryPackageBase import *


class PackageWin(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

    def fetch(self):
        return True

    def unpack(self):
        return True

    def install(self):
        destdir = os.path.join(self.installDir(), "bin")
        utils.createDir(destdir)

        with utils.ScopedEnv({"PATHEXT" : ";".join(f"_{ver}.dll" for ver in range(60, 30, -1))}):
            d3dcompiler = shutil.which("d3dcompiler")
            utils.copyFile(d3dcompiler, os.path.join(destdir, os.path.basename(d3dcompiler)), linkOnly=False)
        return True


from Package.Qt5CorePackageBase import *


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, condition=OsUtils.isWin(), classA=PackageWin)
