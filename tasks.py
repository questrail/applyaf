from invoke import run, task

TESTPYPI = "https://testpypi.python.org/pypi"


@task
def lint():
    """Run flake8 to lint code"""
    run("python setup.py flake8")


@task(lint)
def test():
    """Lint, unit test, and check setup.py"""
    run("nosetests")
    run("python setup.py check")


@task()
def release(deploy=False, test=False, version=''):
    """Tag release, run Travis-CI, and deploy to PyPI
    """
    if test:
        run("python setup.py check")
        run("python setup.py register sdist upload --dry-run")

    if deploy:
        run("python setup.py check")
        if version:
            run("git checkout master")
            run("git tag -a v{ver} -m 'v{ver}'".format(ver=version))
            run("git push")
            run("git push origin --tags")
            run("python setup.py register sdist upload")
    else:
        print("* Have you updated the version in applyaf.py?")
        print("* Have you updated CHANGELOG.md?")
        print("* Have you fixed any last minute bugs?")
        print("If you answered yes to all of the above questions,")
        print("then run `inv release --deploy -vX.YY.ZZ` to:")
        print("- Checkout master")
        print("- Tag the git release with provided vX.YY.ZZ version")
        print("- Push the master branch and tags to repo")
