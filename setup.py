from setuptools import setup, find_packages

__version__ = "0.0.0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = f.read()

setup(
    name="crypto_VDF",
    description="Verifiable Delay Function project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/programmingAthlete/crypto-VDF.git",
    version=__version__,
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["*tests*"]),
    install_requires=requirements,
    zip_safe=True
)
