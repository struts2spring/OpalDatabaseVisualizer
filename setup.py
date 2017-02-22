__author__ = 'vijay'

from setuptools import setup

setup(
    name='opaldatabasevisualizer',
    version='0.1',
    url='https://github.com/struts2spring/OpalDatabaseVisualizer',
    license='BSD',
    author='Vijay',
    author_email='',
    description='Database tool for developers, DBAs and analysts..',
    long_description=__doc__,
    packages=['src','src.view','src.connect','src.view.connection','src.view.history','src.view.worksheet','src.connect.sqlite',
              'src.view.table','src.sqlite_executer','src.SqlBeautifier','src.SqlBeautifier.sqlparse2','src.SqlBeautifier.sqlparse2.engine',
              'src.view.findAndReplace','src.view.preference','src.images'],
    py_modules=['src'],
    zip_safe=False,
    platforms='any',
    install_requires=[
#        'wxPython ==3.0.2.0',
        'SQLAlchemy == 1.0.12',
    ],
    classifiers=[
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Database tool',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
    ],
    
    # What does your project relate to?
    keywords='ebook management ',
    package_data={'src.images':['*.png']},
    include_package_data=True
    )
#!/usr/bin/python
