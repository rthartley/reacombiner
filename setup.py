from setuptools import setup

setup(
    name='ReaCombiner',
    version='0.1.0',
    packages=['ReaCombiner'],
    url='',
    license='',
    author='Roger T. Hartley',
    author_email='roger.t.hartley@gmail.com',
    description='A program to organize Reaper projects in one place and to view their main properties',
    install_requires=['rpp', 'fpdf', 'PySimpleGUI'],
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Reaper users',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3'],
    keywords='reaper project organize view',
    python_requires='>=3',
    package_data={
        'ReaCombiner': ['test/test.RPP', 'test/test-plugins.RPP'],
    }
)
