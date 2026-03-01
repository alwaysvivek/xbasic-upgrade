from setuptools import setup, find_packages
import os
import subprocess
from setuptools.command.install import install

class CustomInstall(install):
    def run(self):
        # Build the C++ compiler during install
        compiler_dir = os.path.join(os.getcwd(), 'xbasic_modern', 'compiler')
        subprocess.check_call(['make', '-C', os.path.dirname(compiler_dir)])
        install.run(self)

setup(
    name="xbasic-modern",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'xb-modern=xbasic_modern.cli:main',
        ],
    },
)
