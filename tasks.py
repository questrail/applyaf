from invoke import task


@task
def build():
    """
    Bump versions and prepare for PyPI
    """
    print("Building!")


@task
def deploy():
    """
    Deploy to PyPI
    """
    print("Deploying to PyPI!")
