import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ["1.8.2"]:
            self.targets[ ver ] = f"ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-{ver}.tar.bz2"
            self.targetInstSrc[ ver ] = f"libgcrypt-{ver}"

        self.targetDigests['1.8.2'] = (['c8064cae7558144b13ef0eb87093412380efa16c4ee30ad12ecb54886a524c07'], CraftHash.HashAlgorithm.SHA256)
        self.description = " General purpose crypto library based on the code used in GnuPG."
        self.defaultTarget = "1.8.2"

    def setDependencies( self ):
        self.buildDependencies["dev-utils/msys"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/gpg-error"] = "default"

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase ):
    def __init__( self ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.configure.args += " --disable-static --enable-shared --disable-asm --disable-padlock-support"


    def install( self ):
        if not AutoToolsPackageBase.install(self):
            return False
        return self.copyToMsvcImportLib()
