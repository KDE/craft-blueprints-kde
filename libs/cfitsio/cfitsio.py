import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['3.08', '3.10', '3.14', '3.20', '3.31', '3.35', '3.45', '3.47']:
            self.targets[ver] = 'http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = "cfitsio-" + ver
        self.targetDigests['3.20'] = 'f200fe0acba210e88e230add6a4e68d80ad3d4f2'
        self.targetDigests['3.31'] = '35360dccc69dc5f12efb6fc9096ad951b59244d5'
        self.targetDigests['3.35'] = 'e928832708d6a5df21a1e17ae4a63036cab7c1b9'
        self.targetDigests['3.45'] = (['bf6012dbe668ecb22c399c4b7b2814557ee282c74a7d5dc704eb17c30d9fb92e'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply['3.20'] = [("cfitsio-20101130.diff", 1)]
        self.patchToApply['3.31'] = [("cfitsio-20130124.diff", 1)]
        self.patchToApply['3.35'] = [("cfitsio-20130124.diff", 1)]
        self.patchToApply['3.45'] = [("cfitsio-3.45-20180706.diff", 1), ("cfitsio-3.45-20180713.diff", 1)]

        self.description = "library for the FITS (Flexible Image Transport System) file format"
        self.defaultTarget = '3.47'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DENABLE_STATIC=ON"
