import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ["1.9.4"]:
            self.targets[ ver ] = f"ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-{ver}.tar.bz2"
            self.targetInstSrc[ ver ] = f"libgcrypt-{ver}"
        self.targetDigests["1.9.4"] = (['ea849c83a72454e3ed4267697e8ca03390aee972ab421e7df69dfe42b65caaf7'], CraftHash.HashAlgorithm.SHA256)

        self.description = " General purpose crypto library based on the code used in GnuPG."
        self.defaultTarget = "1.9.4"

    def setDependencies( self ):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gpg-error"] = None

from Package.AutoToolsPackageBase import *


class Package( AutoToolsPackageBase ):
    def __init__( self ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.configure.args += " --disable-static --enable-shared --disable-asm --disable-padlock-support"
