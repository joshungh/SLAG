from setuptools import setup, find_packages

setup(
    name="slag",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "boto3>=1.34.29",
        "pinecone-client>=2.2.4",
        "python-dotenv>=1.0.0",
        "pytest>=7.4.3",
        "pydantic>=2.5.3",
        "asyncio>=3.4.3",
        "aiohttp>=3.9.1",
        "python-json-logger>=2.0.7"
    ]
) 