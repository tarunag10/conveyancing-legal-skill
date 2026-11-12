"""Include the reference bundle in wheels; editable installs use the source root."""
from pathlib import Path
from shutil import copy2, copytree
from setuptools import setup
from setuptools.command.build_py import build_py

class BuildWithReferences(build_py):
    def run(self):
        super().run()
        root=Path(__file__).parent
        target=Path(self.build_lib)/'conveyancing_skill'/'data'
        target.mkdir(parents=True,exist_ok=True)
        for name in ('knowledge','core','schemas','templates','skills','docs'):
            copytree(root/name,target/name,dirs_exist_ok=True,
                     ignore=lambda directory,names:[n for n in names if n=='.DS_Store' or n=='__pycache__'])
        for name in ('SKILL.md','README.md','plugin.json'):
            copy2(root/name,target/name)

setup(cmdclass={'build_py':BuildWithReferences})
