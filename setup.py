'''
Created on 1 Oct 2020

@author: semuadmin
'''
import setuptools

from pyubx2._version import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyubx2",
    version=VERSION,
    author="semuadmin",
    author_email="semuadmin@semuconsulting.com",
    description="UBX Protocol Parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/semuconsulting/pyubx2",
    packages=setuptools.find_packages(),
    package_data={'': ['ubxlog.bin']},
    include_package_data=True,
    license="BSD 3-Clause 'Modified' License",
    project_urls={
        "Bug Tracker": "https://github.com/semuconsulting/pyubx2",
        "Documentation": "https://github.com/semuconsulting/pyubx2",
        "Source Code": "https://github.com/semuconsulting/pyubx2",
    },
    classifiers=[
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Topic :: Utilities'
    ],
    python_requires='>=3.6',
)
