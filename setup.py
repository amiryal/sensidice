from distutils.core import setup

setup(name='sensidice',
      version='0.1',
      author='Amir Yalon',
      author_email='sensidice@amir.eml.cc',
      url='http://github.com/amiryal/sensidice',
      description='To aid in creating sensible passphrases using dice',
      long_description=__import__('sensidice').__doc__,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Security',
          'Topic :: Security :: Cryptography',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
      ],
      py_modules=['sensidice'],
     )

