from setuptools import setup, find_packages

version = '0.0.1'

setup(name="helga-ansible",
      version=version,
      description=('ansible plugin for helga'),
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ],
      keywords='irc bot ansible',
      author='alfredo deza',
      author_email='contact [at] deza [dot] pe',
      url='https://github.com/alfredodeza/helga-ansible',
      license='MIT',
      packages=find_packages(),
      entry_points = dict(
          helga_plugins = [
              'ansible = helga_ansible:helga_ansible',
          ],
      ),
)
