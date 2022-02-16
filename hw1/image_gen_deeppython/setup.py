import setuptools

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="image_gen_deeppython",
    version="0.0.4",
    author="Alexander Krikun",
    author_email="krikun98@gmail.com",
    description=("A sample graph generator for an advanced Python class"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Unlicense",
    url="http://packages.python.org/image_gen_deeppython",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
    ],
)
