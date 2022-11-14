import io
import re
import setuptools

with io.open("app_properties/__init__.py", encoding="utf-8") as f:
    regex_result = re.search(r"__version__ = \"(.+)\"", f.read())
    version = regex_result.group(1) if regex_result else "0.1.0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-app-properties",
    version=version,
    author="Yaroslav Kikvadze",
    author_email="yaroslav.k@simporter.com",
    description="Java application properties for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yar-kik/py-app-properties",
    license="MIT",
    packages=["app_properties"],
    install_requires=["PyYAML>=6.0"],
    python_requires=">=3.8",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
