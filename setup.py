from setuptools import setup, find_packages

setup(
    name='application-event-logger',
    version='0.1',
    long_description=__doc__,
    py_modules= [],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=['sqlalchemy', 'blinker'],
    test_suite='eventloggertests'
)
