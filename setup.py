from setuptools import setup, find_packages
import os

version = "1.0"

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md")).read()

setup(
    name="lfs-bulk-prices",
    version=version,
    description="Bulk prices for LFS",
    long_description=README,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords="django e-commerce online-shop",
    author="Kai Diefenbach",
    author_email="kai.diefenbach@iqpp.de",
    license="BSD",
    packages=find_packages(exclude=["ez_setup"]),
    include_package_data=True,
    zip_safe=False,
    dependency_links=[],
    install_requires=[
        "setuptools",
    ],
)
