from setuptools import setup, find_packages

setup(
    name='wioleet',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'click_config',
        'flask',
        'requests',
        'schedule',
    ],
    entry_points='''
        [console_scripts]
        wioleet=src.wioleet:cli
    ''',
)