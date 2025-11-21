#!/usr/bin/env python3
"""
Setup script for IPTrack - Security Monitoring Tool
Installs iptrack globally as a command-line tool
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="iptrack-security",
    version="1.0.0",
    description="Professional CLI tool for tracking and blocking unauthorized access attempts with IP geolocation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Defender Security",
    author_email="security@defender.local",
    url="https://github.com/defender/iptrack",
    license="MIT",
    
    # Package configuration
    py_modules=[
        'iptrack',
        'security_monitor',
        'ip_locator',
        'defender_control',
        'quick_start'
    ],
    
    # Dependencies
    install_requires=[
        'requests>=2.25.0',
    ],
    
    # Python version requirement
    python_requires='>=3.7',
    
    # Entry points for CLI commands
    entry_points={
        'console_scripts': [
            'iptrack=iptrack:main',
        ],
    },
    
    # Make iptrack script directly executable
    scripts=['iptrack'],
    
    # Include additional files
    package_data={
        '': ['config.json', 'README.md', 'QUICK_REFERENCE.md'],
    },
    
    # Classification
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console',
    ],
    
    keywords='security monitoring ip-blocking firewall geolocation cli',
    
    project_urls={
        'Documentation': 'https://github.com/defender/iptrack/wiki',
        'Source': 'https://github.com/defender/iptrack',
        'Tracker': 'https://github.com/defender/iptrack/issues',
    },
)
