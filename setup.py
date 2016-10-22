"""
Setup file for gym login
"""
import os

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.md')) as f:
    README = f.read()
with open(os.path.join(HERE, 'CHANGES.txt')) as f:
    CHANGES = f.read()

REQUIRES = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    ]

TESTS_REQUIRE = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
    ]

setup(name='gym_login',
      version='0.0',
      description='gym_login',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': TESTS_REQUIRE,
      },
      install_requires=REQUIRES,
      entry_points="""\
      [paste.app_factory]
      main = gym_login:main
      [console_scripts]
      initialize_gym_login_db = gym_login.scripts.initializedb:main
      """, )
