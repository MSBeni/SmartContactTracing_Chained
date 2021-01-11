from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    INSTALL_REQUIRES = [l.split('#')[0].strip() for l in fh if not l.strip().startswith('#')]

classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python :: 3',
          'Topic :: Communications :: Email',
          'Topic :: Office/Business',
          'Topic :: Software Development :: Bug Tracking',
          ]


setup(name='chainedSCT',
      version='0.0.1',
      description='Blockchain-Based Smart Contact Tracing',
      py_modules=["chainedSCT"],
      # package_dir={'': 'GetTweets'},
      entry_points={'console_scripts': ['chainedSCT = chainedSCT.__main__:main']},
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='MSBeni',
      author_email='andrei.sokurov.bitco@gmail.com',
      # License='MIT',
      classifiers=classifiers,
      keywords='calculator',
      url='https://github.com/MSBeni/SmartContactTracing_Chained',
      packages=find_packages(),
      # install_requiers=[''],
      extras_require={
          "dev": [
              "pytest>=3.7",
          ],
      },
      install_requires=INSTALL_REQUIRES,
     )

