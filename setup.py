#!/usr/bin/env python3
from setuptools import setup, find_packages

PACKAGES = find_packages(exclude=["tests", "tests.*"])

REQUIRES = ["selenium>=3.141.0", "selenium-page-elements==0.1.6"]

PROJECT_CLASSIFIERS = [
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.6",
    "Topic :: Software Development :: Libraries",
]

setup(
    name="draytekwebadmin",
    version="0.0.1",
    license="MIT",
    url="https://github.com/highlight-slm/Draytek-Web-Auto-Configuration",
    download_url="https://github.com/highlight-slm/Draytek-Web-Auto-Configuration",
    author="Martin Rowan",
    author_email="martin@rowannet.co.uk",
    description="Selenium based web API to configure DrayTek routers",
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True,
    platforms="any",
    install_requires=REQUIRES,
    test_suite="tests",
    keywords=["draytek", "selenium"],
    classifiers=PROJECT_CLASSIFIERS,
)
