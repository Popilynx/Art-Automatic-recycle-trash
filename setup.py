from setuptools import setup, find_packages

setup(
    name="classificador_lixo",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'tflite-runtime; platform_system=="Linux" and platform_machine=="aarch64"',  # Raspberry Pi
        'tensorflow; platform_system!="Linux" or platform_machine!="aarch64"',  # Outros sistemas
        'opencv-python',
        'numpy',
        'pillow',
        'RPi.GPIO; platform_system=="Linux" and platform_machine=="aarch64"'  # Raspberry Pi
    ],
    extras_require={
        'dev': [
            'pyinstaller',
            'pytest',
            'pytest-cov',
        ],
    },
    author="Seu Nome",
    author_email="seu.email@exemplo.com",
    description="Sistema de classificação de lixo para Raspberry Pi 4",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='raspberry-pi, machine-learning, waste-classification',
    url='https://github.com/seu-usuario/classificador_lixo',
) 