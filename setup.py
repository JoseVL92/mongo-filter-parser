from setuptools import setup, find_packages

setup(
    name="mongo_filter_parser",
    version="0.1.0",
    packages=find_packages(),
    description="A Python utility for converting URL query parameters into MongoDB filter queries",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="JoseVL92",
    author_email="jovalab92@gmail.com",
    url="https://github.com/JoseVL92/mongo-filter-parser",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    keywords="mongodb, filter, query, parser, url",
)