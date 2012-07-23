from setuptools import setup, find_packages


VERSION = __import__("forms_builder_integration").__version__

setup(
    name="feincms-forms-builder",
    description="Integrate django-forms-builder into FeinCMS.",
    version=VERSION,
    author="Bojan Mihelac",
    author_email="bmihelac@mihelac.org",
    url="https://github.com/bmihelac/feincms-forms-builder",
    license='BSD License',
    install_requires=[
        ],
    packages=find_packages(exclude=["example", "example.*"]),
)
