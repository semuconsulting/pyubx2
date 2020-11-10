'''
Created on 1 Oct 2020

@author: semuadmin
'''
import setuptools

from pyubx2 import version as VERSION

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
    packages=setuptools.find_packages(exclude=['tests', 'examples']),
    license="BSD 3-Clause 'Modified' License",
    keywords="pyubx2 GNSS GPS GLONASS UBX GIS u-blox",
    platforms="Windows, MacOS, Linux",
    project_urls={
        "Bug Tracker": "https://github.com/semuconsulting/pyubx2",
        "Documentation": "https://github.com/semuconsulting/pyubx2",
        "Source Code": "https://github.com/semuconsulting/pyubx2",
    },
    classifiers=[
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: BSD License',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: GIS'
    ],
    python_requires='>=3.6',
)
