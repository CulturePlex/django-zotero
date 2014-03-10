import codecs
import re
from os import path
from setuptools import setup, find_packages


def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return codecs.open(file_path).read()


def find_version(*parts):
    default = '0.2'
    try:
        version_file = read(*parts)
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                                  version_file, re.M)
        if version_match:
            return version_match.group(1)
        else:
            return default
    except:
        return default
#    raise RuntimeError("Unable to find version string.")


setup(
    name='django-zotero',
    version=find_version('django_zotero', '__init__.py'),
    author='Antonio Jimenez Mavillard',
    author_email='ajmavillard@gmail.com',
    url='https://github.com/CulturePlex/django-zotero',
    description='Django tool to tag objects and export them to Zotero',
    long_description=read('README.rst'),
    license='MIT',
    keywords='zotero django admin tag meta metatag',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        ],
    zip_safe=False,
    packages=['django_zotero'],
    include_package_data=True,
    install_requires=['jsonfield'],
)
