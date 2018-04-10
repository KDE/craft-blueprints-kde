import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.11.08", "2.13.03"]:
            if CraftCore.compiler.isWindows:
                self.targets[ver] = f"https://www.nasm.us/pub/nasm/releasebuilds/{ver}/win{CraftCore.compiler.bits}/nasm-{ver}-win{CraftCore.compiler.bits}.zip"
            elif CraftCore.compiler.isMacOS:
                self.targets[ver] = f"https://www.nasm.us/pub/nasm/releasebuilds/{ver}/macosx/nasm-{ver}-macosx.zip"
            self.targetInstSrc[ver] = f"nasm-{ver}"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")

        if CraftCore.compiler.isWindows:
            self.targetDigests['2.11.08'] = 'db67cb1286b01e835b703402d631c88c8f494d6b'
            self.targetDigests['2.13.03'] = (['b3a1f896b53d07854884c2e0d6be7defba7ebd09b864bbb9e6d69ada1c3e989f'], CraftHash.HashAlgorithm.SHA256)

        self.description = "This is NASM - the famous Netwide Assembler"
        self.webpage = "https://www.nasm.us/"
        self.defaultTarget = "2.13.03"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
