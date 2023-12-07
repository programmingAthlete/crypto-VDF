from setuptools import setup, find_packages

__version__ = "0.0.0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

# setup(
#     name="crypto_VDF",
#     version=__version__,
#     description="Verifiable Delay Function project",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/programmingAthlete/crypto-VDF.git",
#     packages=find_packages(where="src", include=["crypto_VDF*"]),
#     package_dir={"": "src"},
#     install_requires=requirements,
#     zip_safe=False
# )
setup(
    name="crypto_VDF",
    version=__version__,
    description="Verifiable Delay Function project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/programmingAthlete/crypto-VDF.git",
    packages=find_packages(where="src", include=["crypto_VDF*"]),
    package_dir={"": "src"},
    console_scripts={
        "cryptoVDF": "crypto_VDF.entry_point:main"},
    install_requires=requirements,
    zip_safe=False
)
