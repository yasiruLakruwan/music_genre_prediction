#-----Setup files 

from setuptools import setup,find_packages
from datetime import datetime

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Music genre predicton",
    version="0.0.1",
    author="Yasiru Lakruwan",
    packages=find_packages(),
    install_requires = requirements
)

