from setuptools import setup, find_packages

setup(
    name="xscraper",            # Name of your package
    version="0.1.0",                 # Version of your package
    description="A package to collect user information, the followers, followings, and tweets of a user, and collect tweets by a given hashtag or keyword on X.",  # Short description
    long_description=open("README.rst").read(),  # Long description from README
    long_description_content_type="text/x-rst",  # Format of the long description
    author="Angelina Voggenreiter, Idil Sezgin",              # Your name
    author_email="angelina.voggenreiter@tum.de, idil.sezgin@tum.de",  # Your email
    url="https://github.com/jpfefferlab/xscraper",  # Link to your GitHub repo
    packages=find_packages(),        # Automatically find subpackages
    install_requires=[
    "beautifulsoup4"
    "python-dateutil",         
    "selenium",               # Selenium for web automation
    "chromedriver-autoinstaller",  # Automatically installs the appropriate ChromeDriver
],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)