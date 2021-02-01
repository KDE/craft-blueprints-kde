import info

from Package.BinaryPackageBase import *
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):

    def setTargets(self):
        for ver in ["2.13.03", "2.14.02"]:
            if CraftCore.compiler.isMSVC():
                self.targets[ver] = f"https://www.nasm.us/pub/nasm/releasebuilds/{ver}/win{CraftCore.compiler.bits}/nasm-{ver}-win{CraftCore.compiler.bits}.zip"
            else:
                self.targets[ver] = f"https://www.nasm.us/pub/nasm/releasebuilds/{ver}/nasm-{ver}.tar.bz2"

            self.targetInstSrc[ver] = f"nasm-{ver}"
            if CraftCore.compiler.isMSVC():
                self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")
            else:
                self.targetInstallPath[ver] = "dev-utils"

        if CraftCore.compiler.isMSVC():
            self.targetDigestsX64['2.14.02'] =  (['18918ac906e29417b936466e7a2517068206c8db8c04b9762a5befa18bfea5f0'], CraftHash.HashAlgorithm.SHA256)

        self.description = "This is NASM - the famous Netwide Assembler"
        self.webpage = "https://www.nasm.us/"
        self.defaultTarget = "2.14.02"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = None

if CraftCore.compiler.isMSVC():
    class Package(BinaryPackageBase):
        def __init__(self):
            BinaryPackageBase.__init__(self)
else:
    class Package(AutoToolsPackageBase):
        def __init__(self):
            AutoToolsPackageBase.__init__(self)

