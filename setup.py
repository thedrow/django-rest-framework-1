#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from Cython.Build import cythonize
except ImportError:
    ext_modules = None
else:
    from setuptools import Extension
    ext_modules = cythonize(Extension('speedups', ['rest_framework/renderers.py',
                                                   'rest_framework/__init__.py',
                                                   'rest_framework/fields.py',
                                                   'rest_framework/mixins.py',
                                                   'rest_framework/generics.py',
                                                   'rest_framework/views.py',
                                                   'rest_framework/serializers.py',
                                                   'rest_framework/pagination.py',
                                                   'rest_framework/parsers.py',
                                                   'rest_framework/negotiation.py']))

import re
import os
import sys

from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


version = get_version('rest_framework')

if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

setup(
    name='djangorestframework',
    version=version,
    url='http://www.django-rest-framework.org',
    license='BSD',
    description='Web APIs for Django, made easy.',
    author='Tom Christie',
    author_email='tom@tomchristie.com',  # SEE NOTE BELOW (*)
    packages=get_packages('rest_framework'),
    package_data=get_package_data('rest_framework'),
    install_requires=[],
    zip_safe=False,
    ext_modules=ext_modules,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ]
)

# (*) Please direct queries to the discussion group, rather than to me directly
# Doing so helps ensure your question is helpful to other users.
# Queries directly to my email are likely to receive a canned response.
#
#     Many thanks for your understanding.
