from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="puzzle3d",
    version="0.1.0",
    author="3DPuzzle Contributors",
    description="A tool to transform 3D objects into interlocking 3D puzzles for wood manufacturing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24.0",
        "trimesh>=3.23.0",
        "numpy-stl>=2.17.0",
        "scipy>=1.10.0",
        "shapely>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "puzzle3d=puzzle3d.cli:main",
        ],
    },
)
