from Package.CMakePackageBase import *

class Pattern(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-DINSTALL_PUBLICBINDIR=bin"]


    def install(self):
        if not super().install():
            return False
        user_facing_tool_links = self.buildDir() / "user_facing_tool_links.txt"
        if user_facing_tool_links.exists():
            with user_facing_tool_links.open("rt") as links:
                for line in links:
                    line = line.strip()
                    if not line:
                        continue
                    src, dest = line.split()
                    src = Path(src).relative_to(CraftCore.standardDirs.craftRoot()).with_suffix(CraftCore.compiler.executableSuffix)
                    if not utils.createShim(self.installDir() / dest,  self.installDir() / src):
                        return False
        if CraftCore.compiler.isWindows:
            # TODO: there must be a more elegant way
            dll = utils.filterDirectoryContent(self.installDir() / "lib/qt6/bin",
                                                    whitelist=lambda x, root: x.name.endswith(".dll"),
                                                    blacklist=lambda x, root: True)
            utils.createDir(self.installDir() / "bin")
            for d in dll:
                src = Path(d)
                if not utils.copyFile(src, self.installDir() / "bin" / src.name):
                    return False
                src = src.with_suffix(".pdb")
                if src.exists():
                    if not utils.copyFile(src, self.installDir() / "bin" / src.name):
                        return False
        return True