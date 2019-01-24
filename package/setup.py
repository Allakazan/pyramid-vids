from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'pyramid',
    'pyramid_chameleon',
    'waitress',
    'pymongo',
]

setup(
    name='pyramid-interview',
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = app:main'
        ],
    },
)