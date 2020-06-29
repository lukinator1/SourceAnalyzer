import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="source-analyzer-pkg-dcaust1n",
    version="0.0.1",
    author="Djoni Austin",
    author_email="dcaustin@ufl.edu",
    description="Compare coding files for similarities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dcaust1n/SourceAnalyzer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)