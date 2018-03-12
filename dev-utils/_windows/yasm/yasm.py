import info


class subinfo(info.infoclass):
    def setTargets(self):
        if CraftCore.compiler.isX64():
            if CraftCore.compiler.isMinGW():
                self.targets['1.2.0'] = "http://www.tortall.net/projects/yasm/releases/yasm-1.2.0-win64.exe"
            if CraftCore.compiler.isMSVC():
                self.targets['1.2.0'] = "http://www.tortall.net/projects/yasm/releases/vsyasm-1.2.0-win64.zip"
        else:
            if CraftCore.compiler.isMinGW():
                self.targets['1.2.0'] = "http://www.tortall.net/projects/yasm/releases/yasm-1.2.0-win32.exe"
            if CraftCore.compiler.isMSVC():
                self.targets['1.2.0'] = "http://www.tortall.net/projects/yasm/releases/vsyasm-1.2.0-win32.zip"

        self.targetInstallPath["1.2.0"] = os.path.join("dev-utilss", "bin")
        self.description = "The Yasm Modular Assembler Project"
        self.defaultTarget = '1.2.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        ## @todo remove the readme.txt file

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        if CraftCore.compiler.isMinGW_W32():
            shutil.move(os.path.join(self.installDir(), "yasm-1.2.0-win32.exe"),
                        os.path.join(self.installDir(), "yasm.exe"))
        if CraftCore.compiler.isMinGW_W64():
            shutil.move(os.path.join(self.installDir(), "yasm-1.2.0-win64.exe"),
                        os.path.join(self.installDir(), "yasm.exe"))

        return True
