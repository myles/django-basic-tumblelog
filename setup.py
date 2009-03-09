from distutils.core import setup
import os

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
	os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('tumblelog'):
	# Ignore dirnames that start with '.'
	for i, dirname in enumerate(dirnames):
		if dirname.startswith('.'): del dirnames[i]
	if '__init__.py' in filenames:
		pkg = dirpath.replace(os.path.sep, '.')
		if os.path.altsep:
			pkg = pkg.replace(os.path.altsep, '.')
		packages.append(pkg)
	elif filenames:
		prefix = dirpath[10:] # Strip "tumblelog/" or "tumblelog\"
		for f in filenames:
			data_files.append(os.path.join(prefix, f))

setup(
	name = 'django-basic-tumblelog',
	version = '0.5',
	description = 'Django Basic Tumblelog',
	author = 'Myles Braithwaite',
	author_email = 'me@mylesbraithwaite.com',
	package_dir = {
		'tumblelog': 'tumblelog',
	},
	packages = packages,
	package_data = {
		'tumblelog': data_files,
	}
)