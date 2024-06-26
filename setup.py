from setuptools import setup, find_packages

setup(
    name="timesheet",
    version="0.1.0",
    author="Ben Clews",
    author_email="your.email@example.com",
    description="A CLI application for recording and tracking timesheets.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bclews/timesheet",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer[all]",
    ],
    entry_points={
        "console_scripts": [
            "timesheet=flex_timesheet.cli:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="GPL-3.0-or-later",
)
