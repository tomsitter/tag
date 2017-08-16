from setuptools import setup

setup(
    name='tag',
    packages=['tag'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-restplus',
        'geoalchemy2',
        'Pillow',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    extras_require={
        'dev': [
            'sqlalchemy-migrate',
        ]
    }
)
