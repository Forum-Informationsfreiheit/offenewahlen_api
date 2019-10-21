from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

CLASSIFIERS = [
    #'Development Status :: 1 - ',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: All',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Open Data',
    'Topic :: Elections',
    'Programming Language :: Python :: 3.5',
    'Framework :: Django',
    'Framework :: Django :: 1.11',
]

INSTALL_REQUIREMENTS = [
    'Django==1.11.23'
]

setup(
    author='Stefan Kasberger',
    author_email='info@offenewahlen.at',
    name='offenewahlen_api',
    version='0.1',
    #version=cms.__version__,
    description='Open Election Data API from Austria.',
    long_description=README,
    url='https://offenewahlen.at/',
    license='MIT License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIREMENTS,
    packages=find_packages(exclude=['project', 'project.*']),
    include_package_data=True,
    zip_safe=False,
    #test_suite='runtests.main',
)
