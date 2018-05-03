import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ["2.4.3", "2.5.1"]:
            self.targets[ ver ] = f"https://www.gnupg.org/ftp/gcrypt/libassuan/libassuan-{ver}.tar.bz2"
            self.targetInstSrc[ ver ] = f"libassuan-{ver}"

        self.targetDigests['2.4.3'] = (['22843a3bdb256f59be49842abf24da76700354293a066d82ade8134bb5aa2b71'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.5.1"] = (['47f96c37b4f2aac289f0bc1bacfa8bd8b4b209a488d3d15e2229cb6cc9b26449'], CraftHash.HashAlgorithm.SHA256)

        self.description = "An IPC library used by some of the other GnuPG related packages"
        self.defaultTarget = "2.5.1"

    def setDependencies( self ):
        self.buildDependencies["dev-utils/msys"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/gpg-error"] = "default"

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )

    def install( self ):
        if not AutoToolsPackageBase.install(self):
            return False
        return self.copyToMsvcImportLib()
