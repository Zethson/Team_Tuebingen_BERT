#!/usr/bin/env python

from setuptools import setup, find_packages

version = '0.1dev'

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='BERT',
    version=version,
    description='Deimmunization workflow',
    long_description=readme,
    keywords=['deimmunization'],
    author='IGEM-Tuebingen-2018',
    author_email='igem@ifib.uni-tuebingen.de',
    license=license,
    scripts=['scripts/BERT'],
    install_requires=required,
    packages=find_packages(exclude='docs'),
    include_package_data=True,
    data_files=[('data/inputfiles', ['data/inputfiles/contact_blomap_7A.csv']),
                ('data', ['data/2wcv.pdb']),
                ('data', ['data/dataset_S2648_edited_tsv.csv']),
                ('data', ['data/isomerase_90_similarity.clustal_num'])
    ]
)
