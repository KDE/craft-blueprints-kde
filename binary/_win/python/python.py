import info
from CraftCompiler import CraftCompiler


class subinfo(info.infoclass):
    def setTargets(self):
        arch = "win32"
        if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
            arch = "amd64"
            self.targetDigests["3.6.6"] = (["d294ed2a18bb2fb822a1be346af79a48980eb0d3d5f209cf9e728e93883b565a"], CraftHash.HashAlgorithm.SHA256)
            self.targetDigests["3.7.0"] = (["0cc08f3c74c0112abc2adafd16a534cde12fe7c7aafb42e936d59fd3ab08fcdb"], CraftHash.HashAlgorithm.SHA256)

        for ver in ["3.6.6", "3.7.0"]:
            self.targets[ver] = f"https://www.python.org/ftp/python/{ver}/python-{ver}-embed-{arch}.zip"
            self.targetInstallPath[ver] = "python"
        self.defaultTarget = "3.6.6"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        # https://bugs.python.org/issue29319
        files = os.listdir(self.installDir())
        reZipName = re.compile(r"python\d\d.*")
        name = None
        for f in files:
            if reZipName.match(f):
                name, _ = os.path.splitext(f)
                break
        return utils.deleteFile(os.path.join(self.installDir(), f"{name}._pth"))
