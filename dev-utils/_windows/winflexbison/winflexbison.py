import info


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "2.5.14"
        self.targets[ver] = f"https://downloads.sourceforge.net/sourceforge/winflexbison/win_flex_bison-{ver}.zip"
        self.targetInstallPath[ver] = os.path.join("dev-utilss", "bin")
        self.targetDigests[ver] = 'e15a1b8780a36ffda9ef70c4f09283867b32a12b'
        self.defaultTarget = ver

    def setDependencies(self):
        self.buildDependencies["gnuwin32/wget"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self): return False
        return \
            utils.copyFile(os.path.join(self.installDir(), "win_flex.exe"),
                           os.path.join(self.installDir(), "flex.exe")) and \
            utils.copyFile(os.path.join(self.installDir(), "win_bison.exe"),
                           os.path.join(self.installDir(), "bison.exe"))
