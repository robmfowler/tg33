from setuptools import setup

setup(
    name = 'tg33',
    version = '0.0.0',
    packages = ['tg33'],
    entry_points = {
        'console_scripts': [
            'tg33 = tg33.__main__:main'
        ]
    }
)