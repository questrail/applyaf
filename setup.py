from distutils.core import setup
setup(
    name='applyaf',
    version='0.1.0',
    author='Matthew Rankin',
    author_email='matthew@questrail.com',
    py_modules=['applyaf'],
    url='http://github.com/questrail/applyaf',
    license='LICENSE.txt',
    description='Apply antenna factor and cable loss to'
        + 'spectrum analyzer measurements',
    requires=['numpy (>=1.6.0)'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
