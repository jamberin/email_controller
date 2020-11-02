import setuptools

with open('README.md', 'r') as read_me:
    description = read_me.read()

setuptools.setup(
    name='email_controller',
    version='0.0.13',
    author='James Beringer',
    author_email='jamberin@gmail.com',
    description='Package for just basic SMTP email sending',
    long_description=description,
    long_description_content_type='text/markdown',
    url='https://github.com/jamberin/email_controller',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Development Status :: 2 - Pre-Alpha',
        'License :: Public Domain'
    ],
    include_package_data=True
)
