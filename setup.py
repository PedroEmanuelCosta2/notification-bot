from setuptools import setup

setup(name='notification-bot',
      version='0.006471',
      description='Discord bot who remind you some tasks',
      url='https://github.com/PedroEmanuelCosta2/notification-bot/',
      author='Pedro Costa & Killian Castella',
      license='https://opensource.org/licenses/BSD-3-Clause',
      packages=['bot'],
      install_requires=(
        'aiohttp>=2.1.0'
        )
)