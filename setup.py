from setuptools import setup, find_packages
import os

# Read the contents of the README file
def read_readme():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'DOC_README.md'), encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

setup(
    name='mkdocs_quizz',
    version='0.0.2',
    description='A MkDocs plugin to create quiz',
    author_email='benjamin@proton.me',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'mkdocs>=1.0.4',
        'beautifulsoup4>=4.11.1',
        'lxml>=4.9.1',
        'pytest>=7.4.4'
    ],
    entry_points={
        'mkdocs.plugins': [
            'mkdocs_quizz = mkdocs_quiz.plugin:QuizPlugin'
        ]
    },
    keywords='mkdocs plugin quiz',
    license='MIT',
    project_urls={
        'Bug Reports': 'https://github.com/bdllard/mkdocs_quiz/issues',
        'Source': 'https://github.com/bdallard/mkdocs_quiz',
    },

)

