from setuptools import setup, find_packages

setup(
    name="cinematic-ai",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyyaml>=6.0",
        "pillow>=10.0.0",
        "numpy>=1.24.0",
        "gtts>=2.3.0",
        "pydub>=0.25.1",
        "moviepy>=1.0.3",
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "cinematic-ai=cinematic_ai.cli:main",
        ],
    },
    python_requires=">=3.8",
)
