from setuptools import find_packages,setup
from typing import List


def get_requirements(file_path:str)->List[str]:
    '''
        Returns a list of the requirements
    '''
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [r.replace('\n','') for r in requirements]
    
    if '-e .' in requirements:
        requirements.remove('-e .')
    
    return requirements


setup(
    name='StuDash',
    version='0.1',
    author='Harounnn',
    author_email='medharoun.1919@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)