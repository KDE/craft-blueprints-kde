import info
from Package.AutoToolsPackageBase import *
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for v in ["0.1.9", "0.2.1"]:
            self.targets[v] = "https://github.com/libsndfile/libsamplerate/archive/" + v + ".tar.gz"
            self.targetInstSrc[v] = "libsamplerate-" + v
        if not CraftCore.compiler.isGCCLike():
            self.patchToApply["0.1.9"] = ("libsamplerate-0.1.9-20180928.diff", 1)
        self.targetDigests["0.1.9"] = "ed60f957a4ff87aa15cbb1f3dbd886fa7e5e9566"
        self.targetDigests["0.2.1"] = (["c28dc9fd587f250114d35aab180e41551935e37c84e7641c31d225cda5eb5fab"], CraftHash.HashAlgorithm.SHA256)
        self.description = "an audio sample rate converter library"
        self.defaultTarget = "0.2.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


if CraftCore.compiler.isGCCLike():

    class Package(AutoToolsPackageBase):
        def __init__(self):
            AutoToolsPackageBase.__init__(self)
            self.subinfo.options.configure.args += ["--disable-static", "--disable-sndfile"]

else:

    class Package(CMakePackageBase):
        def __init__(self):
            CMakePackageBase.__init__(self)
            self.subinfo.options.dynamic.buildTests = False
            self.subinfo.options.configure.args += ["-DLIBSAMPLERATE_EXAMPLES=OFF"]
