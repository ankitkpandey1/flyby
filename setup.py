#!/usr/bin/env python
from __future__ import annotations

from distutils.core import setup

dependencies = ["redis>=2.0,<5.0", "pytest>=7.1.2", "pydantic[dotenv]>=1.9.1"]

setup(
    name="flyby",
    version="1.0",
    description="Provides async task processing with dynamic queues",
    author="Ankit Kumar Pandey",
    author_email="ankitpandey1@gmail.com",
    python_requires=">=3.7",
    install_requires=dependencies,
    url="mammoth.io",
    packages=["flyby", "flyby.common", "flyby.brokers"],
    scripts=["bin/flyby"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Distributed Computing",
    ],
)
