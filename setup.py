from setuptools import setup, find_packages

setup(
    name='common_models',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy'
    ]
)
