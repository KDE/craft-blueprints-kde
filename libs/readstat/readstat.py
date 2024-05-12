import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/WizardMac/ReadStat.git"
        for ver in ["1.1.6", "1.1.8", "1.1.9"]:
            self.targets[ver] = f"https://github.com/WizardMac/ReadStat/releases/download/v{ver}/readstat-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"readstat-{ver}"
        self.targetDigests["1.1.6"] = (["4b80558ab966ec0e0841b7359ee0b91a647a74f02b1b8816313c6f17ce663511"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.1.8"] = (["b18a0d68059d9665491e53838b3ca89b06c3bdaa3b0a11d4ba87d830b743e178"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.1.9"] = (["3a232b9e852d10173e2f25da9155afe2e129a30d1fc6c9aac142cdc5cbfe527e"], CraftHash.HashAlgorithm.SHA256)
        self.description = "A command-line tool and MIT-licensed C library for reading files from popular stats packages"

        self.patchToApply["1.1.8"] = [
            ("211c342a1cfe46fb7fb984730dd7a29ff4752f35.patch", 1),  # Add missing `void` to make Clang happy (*.c files)
            ("5ad80040b94b667e2fef74e9b8d865f142fec820.patch", 1),  # Add missing `void` to make Clang happy (*.h files)
        ]

        if CraftCore.compiler.isMSVC():
            self.patchToApply["1.1.6"] = [("readstat-1.1.6-compiler-flags.diff", 1)]
            self.patchToApply["1.1.8"] += [("readstat-1.1.6-compiler-flags.diff", 1)]

        self.patchLevel["1.1.9"] = 1

        self.defaultTarget = "1.1.9"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/iconv"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--disable-shared"]
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.make.supportsMultijob = False
