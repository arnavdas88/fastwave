from setuptools import find_packages, setup

# from sphinx.setup_command import BuildDoc

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fastwave",
    version="0.1.0",
    description="Build UIs faster, with h2o-wave and fastapi.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arnavdas88/fastwave",
    project_urls={
        "GitHub": "https://github.com/arnavdas88/fastwave",
        "Homepage": "https://github.com/arnavdas88/fastwave",
    },
    author="Arnav Das",
    author_email="arnav.das88@gmail.com",
    keywords="h2o-wave fastapi ui web h2o-lightwave",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        # Testing and Linting Automation
        "nox",
        # Python test
        "pytest",
        # H2O wave UI framework
        "h2o-wave",
        "h2o-lightwave[web]",
        # FastAPI
        "fastapi",
        "jinja2",
        "uvicorn",
        "websockets",
        # Data for examples
        "faker",
        "psutil",
    ],
    classifiers=[
        # License
        "License :: OSI Approved :: MIT License",
        # Project Maturity
        "Development Status :: 3 - Alpha",
        # Topic
        "Topic :: Communications",
        # Compatibility
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        # Python Version
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        # Intended Audience
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        # Framework
        "Framework :: FastAPI",
    ],
)
