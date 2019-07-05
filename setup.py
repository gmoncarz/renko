import io
import os.path

from setuptools import setup


readme_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')


setup(
    name='renko',
    version='0.3.0',
    description='Renko for Python',
    long_description_content_type="text/markdown",
    long_description=io.open(readme_file, 'rt', encoding='utf-8').read(),
    url='https://github.com/gmoncarz/renko',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX',
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries',
    ],
    keywords="renko finance",
    author="Gabriel Moncarz",
    author_email="gabo@moncarz.com.ar",
    zip_safe=False,
    packages=['tests'],
    py_modules=['renko', 'renko_fast'],
    platforms=["POSIX"],
    test_suite="tests",
)
