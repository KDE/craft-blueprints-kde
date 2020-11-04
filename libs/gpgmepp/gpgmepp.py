import info


class subinfo(info.infoclass):
    def setTargets(self):
        for v in ['1.11.1']:
            self.targets[v] = 'https://www.gnupg.org/ftp/gcrypt/gpgme/gpgme-' + v + '.tar.bz2'
            self.targetInstSrc[v] = 'gpgme-' + v
        self.targetDigests['1.11.1'] = (['2d1b111774d2e3dd26dcd7c251819ce4ef774ec5e566251eb9308fa7542fbd6f'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply['1.11.1'] = ("gpgme-1.11.1-20201101.diff", 1)

        self.description = "GnuPG Made Easy - high level crypto API"
        self.defaultTarget = '1.11.1'

    def setDependencies(self):
        self.buildDependencies["libs/assuan2"] = None
        self.buildDependencies["libs/gpg-error"] = None
        self.buildDependencies["libs/gpgme"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gnupg"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        # use openssl for encryption
        self.subinfo.options.configure.args += "-DWITH_CPP=ON -DWITH_QT=ON -DBUILD_SHARED_LIBS=ON"
