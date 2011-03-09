from setuptools import setup, find_packages

setup(
    name='panya-socialcomments',
    description='Facebook style commenting for Panya',
    version='0.0.1',
    author='Hedley Roos',
    author_email='hedleyroos@gmail.com',
    license='BSD',
    url='http://github.com/hedleyroos/panya-socialcomments',
    packages = find_packages(),
    dependency_links = [
    ],
    install_requires = [
        'panya',
        'django-secretballot',
    ],
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
