from setuptools import setup, find_packages

with open('requirements.txt', 'r') as reqs:
    requirements = reqs.readlines()

with open("README.md", 'r') as fyle:
    readme = "\n".join(fyle.readlines())

setup(
    name="redis_alchemy",
    description = "redis_alchemy is a thin wrapper over redis python library"
                  "that makes the api more ergonomic to use for a pythonista."
                  "It is inspired by sqlalchemy, hence the name. But this is"
                  "not an ORM.",
    author="Danish Abdullah",
    author_email="dev@danishabdullah.de",
    version="0.01",
    url="https://github.com/rocket-om/redis_alchemy",
    license="Open Source - 3 clause BSD",
    long_description=readme,
    packages=find_packages(),
    package_dir={"redis_alchemy": "redis_alchemy"},
    install_requires=requirements,
    zip_safe=False,
    keywords="redis",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ]
)