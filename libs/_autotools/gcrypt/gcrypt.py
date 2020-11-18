import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ["1.8.2","1.8.7"]:
            self.targets[ ver ] = f"ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-{ver}.tar.bz2"
            self.targetInstSrc[ ver ] = f"libgcrypt-{ver}"

        self.targetDigests['1.8.2'] = (['c8064cae7558144b13ef0eb87093412380efa16c4ee30ad12ecb54886a524c07'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.8.7'] = (['03b70f028299561b7034b8966d7dd77ef16ed139c43440925fe8782561974748'], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["1.8.7"] = 3
        self.description = " General purpose crypto library based on the code used in GnuPG."
        self.defaultTarget = "1.8.7"

    def setDependencies( self ):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gpg-error"] = None

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase ):
    def __init__( self ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.configure.args += " --disable-static --enable-shared --disable-asm --disable-padlock-support"
