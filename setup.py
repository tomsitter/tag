from setuptools import setup

setup(
    name='tag',
    packages=['tag'],
    include_package_data=True,
    install_requires=[
        'flask',
        'Pillow'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
