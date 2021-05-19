import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="diddiparser",
    version="1.1.0",
    author="Diego Ramirez",
    author_email="dr01191115@gmail.com",
    description="Parser for DiddiScript files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diddileija/diddiparser/blob/main/README.md",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows 8",
        "Topic :: Software Development"
    ],
    keywords="diddi diddiscript script files parse python",
    python_requires='>=3.6, <3.10',
    project_urls={
        "Documentation": "http://github.com/diddileija/diddiparser/blob/main/README.md",
        "Tracker": "http://github.com/diddileija/diddiparser/issues"
    },
    entry_points={
        "console_scripts": [
            "diddiparser=diddiparser.main:main"
        ]
    }  
)
