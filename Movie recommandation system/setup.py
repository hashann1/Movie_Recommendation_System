from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

AUTHOR_NAME = 'Hashan Indeewara'
PACKAGE_NAME = 'src' 
LIST_OF_REQUIREMENTS = ['streamlit']

setup(
    name=PACKAGE_NAME,
    version='0.0.1',
    author=AUTHOR_NAME,
    author_email='weerasinghehashan7@gmail.com',
    description='IRWA - Movie recommendation system',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(), 
    python_requires='>=3.7',
    install_requires=LIST_OF_REQUIREMENTS,
)
