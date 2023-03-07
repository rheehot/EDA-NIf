import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="edanif",
    version="0.1.3",
    author="parkminwoo",
    author_email="parkminwoo1991@gmail.com",
    description="EDA-NIf creates a dataframe containing meta information of NIfTi files and provides several useful features.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DSDanielPark/EDA-NIf",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        "nibabel",
        "pandas",
        "numpy",
        "matplotlib",
        "tqdm",
        "SimpleITK",
        "monai"
    ])