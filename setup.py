from setuptools import find_namespace_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install

requirements = [
    "requests==2.25.1",
    "jsonschema==3.2.0",
    "strict-rfc3339==0.7",
    "dataclasses-json==0.5.3",
]

test_requirements = [
]


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)


setup(
    name="amp-mans-call",
    version="0.1",
    packages=find_namespace_packages(include=["amp.*"], exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=requirements,
    tests_require=test_requirements,
    extras_require={"test": test_requirements},
    cmdclass={"install": PostInstallCommand, "develop": PostDevelopCommand},
)
