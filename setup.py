import io
import re
import setuptools

with io.open("app_properties/__init__.py", encoding="utf-8") as f:
    regex_result = re.search(r"__version__ = \"(.+)\"", f.read())
    version = regex_result.group(1) if regex_result else "0.1.0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="conjector",
    version=version,
    author="Yaroslav Kikvadze",
    author_email="yaroslav.kikvadze@gmail.com",
    description="Config injector for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yar-kik/conjector",
    license="MIT",
    packages=["app_properties"],
    python_requires=">=3.8",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    extras_require={
        "yaml": ["PyYAML>=6.0"],
        "toml": ["toml>=0.10.0"],
        "json": ["ujson>=5.0.0"],
    },
    package_data={"app_properties": ["py.typed"]},
)
