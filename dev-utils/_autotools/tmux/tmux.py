import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ["3.0"]:
            self.targets[ ver ] = f"https://github.com/tmux/tmux/releases/download/{ver}/tmux-{ver}.tar.gz"
            self.targetInstSrc[ ver ] = f"tmux-{ver}"
        self.targetDigests["3.0"] = (['9edcd78df80962ee2e6471a8f647602be5ded62bb41c574172bb3dc3d0b9b4b4'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.0"

    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = None

from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
