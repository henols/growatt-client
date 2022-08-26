#!/usr/bin/env python
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="GrowattClient",
    version="0.0.1",
    description=(
        "Python wrapper for getting data asynchronously "
        "from Growatt inverters "
        "via RS232 or RS485 connection and modbus RTU protocol."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/henols/growatt-client",
    author="Henrik Olsson",
    author_email="henols@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
    ],
    keywords="growatt rs485 rs232 modbus",
    packages=find_packages(),
    python_requires=">=3.6, <4",
    install_requires=["pymodbus"],
    include_package_data=True,
    # fmt: off
    project_urls={
        "Bug Reports":
        "https://github.com/henols/growatt-client/issues",
        "Source":
        "https://github.com/henols/growatt-client",
    },
    # fmt: on
)
