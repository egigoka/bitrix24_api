import setuptools

__version__ = "undefined"  # if setup fails read it from _version.py and to please PyCharm
exec(open('bitrix24api/_version.py').read())

setuptools.setup(
    name='bitrix24api',
    version=__version__,
    packages=['bitrix24api'],
    install_requires=['commands'],
    author='egigoka',
    description='Bitrix24 small and dirty api wrapper',
    long_description="Bitrix24 small and dirty api wrapper"
)
