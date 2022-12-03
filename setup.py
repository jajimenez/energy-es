"""Energy-ES - Setup."""

import setuptools as st

from src.energy_es import __version__ as version


if __name__ == "__main__":
    with open("README.md") as f:
        long_desc = f.read()

    with open("requirements.txt") as f:
        requirements = [i.replace("\n", "") for i in f.readlines()]

    st.setup(
        name="energy-es",
        version=version,
        description=(
            "Desktop application that displays the hourly energy prices for "
            "the current day in Spain."
        ),
        author="Jose A. Jimenez",
        author_email="jajimenezcarm@gmail.com",
        license="MIT",
        long_description=long_desc,
        long_description_content_type="text/markdown",
        url="https://github.com/jajimenez/energy-es",
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: MIT License"
        ],
        python_requires=">=3.9.0",
        install_requires=requirements,
        packages=[
            "energy_es"
        ],
        package_dir={
            "energy_es": "src/energy_es"
        },
        entry_points={
            "console_scripts": [
                "energy-es=energy_es:main"
            ]
        }
    )
