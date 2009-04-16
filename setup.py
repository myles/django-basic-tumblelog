from setuptools import setup, find_packages

setup(
	name = "django-basic-tumblelog",
	version = "1.0",
	url = 'http://myles.github.com/django-basic-tumblelog/',
	license = 'Apache 2.0',
	description = "A basic tumblelog application you can add to your Django website.",
	author = 'Myles Braithwaite',
	packages = find_packages('src'),
	package_dir = {'': 'src'},
	install_requires = ['setuptools'],
)