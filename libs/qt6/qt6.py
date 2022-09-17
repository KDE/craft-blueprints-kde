from Package.CMakePackageBase import *

class Pattern(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-DINSTALL_PUBLICBINDIR=bin"]

    @property
    def qt6EnvBuildEnv(self):
        if CraftCore.compiler.isWindows:
            return {"PATH": f"{self.buildDir() / 'lib/qt6/bin'};{os.environ['PATH']}"}
        return {}

    def make(self):
        with utils.ScopedEnv(self.qt6EnvBuildEnv):
            super().make()

    def postInstall(self):
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
                if not utils.moveFile(src, self.installDir() / "bin" / src.name):
                    return False
                src = src.with_suffix(".pdb")
                if src.exists():
                    if not utils.moveFile(src, self.installDir() / "bin" / src.name):
                        return False
            # we moved the dlls, now lets fix the location in the cmake files
            pattern = re.compile(br"lib/qt6/bin/(.*\.dll)")
            cmake = utils.filterDirectoryContent(self.installDir() / "lib/cmake",
                                                    whitelist=lambda x, root: x.name.endswith(".cmake"),
                                                    blacklist=lambda x, root: True)
            for p in cmake:
                p = Path(p)
                with p.open("rb") as f:
                    content = f.read()
                with p.open("wb") as f:
                    content = pattern.sub(br"bin/\1", content)
                    f.write(content)
        return True