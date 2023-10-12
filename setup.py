from setuptools import setup

setup(
    name='case_study_tebarf_202310_kb',
    version='0.1',
    packages=['case_study_tebarf_202310_kb'],
    url='',
    install_requires=[
        "pandas==2.1.1",
        "transformers==4.34.0"
    ],
    python_requires = '>3.9',
    license='Apache License 2.0',
    author='kbasibuyuk',
    author_email='kubilay.basibuyuk@gmail.com',
    description='Intent and Sentiment Analysis from generated conversations'
)
