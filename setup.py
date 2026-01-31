from setuptools import setup, find_packages

# Konfiguracja pakietu Cinematic AI
setup(
    name="cinematic-ai",                         # Nazwa projektu
    version="0.1.0",                             # Wersja projektu
    packages=find_packages(where="src"),         # Główne źródło kodu (src)
    package_dir={"": "src"},
    install_requires=[
        "pyyaml>=6.0",                           # Konfiguracje YAML
        "pillow>=10.0.0",                        # Manipulacje zdjęciowe i biblioteka dla TTS
        "numpy>=1.24.0", # operacye...