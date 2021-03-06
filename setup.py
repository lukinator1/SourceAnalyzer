import setuptools
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding='utf-8' ) as fh:
    long_description = fh.read()

setuptools.setup(
    name="source_analyzer",
    version="0.1.4", 
    author="Codalyzers",
    author_email="djoni.austin@gmail.com",
    description="Application for analysis of similarities between separate files. Currently with '*.py' and '*.txt' file checking capability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dcaust1n/SourceAnalyzer",
#    package_dir={"": "source_analyzer"},
    packages=setuptools.find_packages(), #where='source_analyzer'
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        "": ["test_files/*.txt","test_files/*.py"],
    },
    entry_points={
        'console_scripts': [
            'source_analyzer=source.source_analyzer:main',
        ],
    },
)