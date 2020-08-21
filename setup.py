try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

setup(name='todo',
      version='0.4',
      description='A dirt simple todo command that uses the todo.txt format and plain text files',
      license='MIT',
      keywords='todo, command line',
      author='Michael Kowalchik',
      author_email='mikepk@tenzerolab.com',
      packages=find_packages(),
      package_data={},
      entry_points={'console_scripts': ['todo=todo.todo_cl:run']})
