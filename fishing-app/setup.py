"""Setup script for 千鱼千寻 OpenClaw Skills"""
from setuptools import setup, find_packages

setup(
    name="qianyuqianxun-openclaw",
    version="2.0.0",
    description="千鱼千寻 OpenClaw Skills - Fishing Mini-Program Backend",
    author="Agent_Pro Team",
    python_requires=">=3.10",
    packages=find_packages(include=["shared", "shared.*", "cli", "cli.*", "mcp_servers", "mcp_servers.*", "skills", "skills.*"]),
    install_requires=[
        "click>=8.1.0",
        "python-dotenv>=1.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
        ],
        "mcp": [
            "mcp>=0.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fishing-cli=cli.main:fishing_cli",
        ],
    },
    package_data={
        "skills": ["*/SKILL.md", "*/README.md"],
    },
    include_package_data=True,
)
