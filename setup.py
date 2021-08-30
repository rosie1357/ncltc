from setuptools import setup, find_packages

setup(
    name='nctcl_project_code',
    version='0.1.0',
    description='Package to create NC database tables/measures/anaylsis',
    packages=find_packages("nc_code"), 
    package_dir={"": "nc_code"},
    author='Rosalie Malsberger', 
    author_email='rmalsberger@mathematica-mpr.com',
    license='Mathematica',
    entry_points={
        'console_scripts': [
            # add when ready
        ],
    },
)