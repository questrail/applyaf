# -*- coding: utf-8 -*-
# Copyright (c) 2022–2024 The applyaf developers. All rights reserved.
# Project site: https://github.com/questrail/applyaf
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Invoke based tasks for applyaf"""

from invoke import task
from unipath import Path

ROOT_DIR = Path(__file__).ancestor(1)


@task
def lint(c):
    """Run ruff to lint code"""
    c.run("ruff check")


@task
def freeze(c):
    """Freeze the pip requirements using pip-chill"""
    c.run(f"pip-chill > {Path(ROOT_DIR, 'requirements.txt')}")


@task(lint)
def test(c):
    """Lint and run unit tests"""
    c.run("nose2 -C")


@task
def outdated(c):
    """List outdated packages"""
    c.run("pip list --outdated")


@task()
def release(c, deploy=False, version=""):
    """Tag release and deploy to PyPI"""
    if deploy and version:
        c.run("git checkout master")
        c.run("git tag -a v{ver} -m 'v{ver}'".format(ver=version))
        c.run("git push")
        c.run("git push origin --tags")
        c.run("hatch build")
        c.run("hatch publish")
    else:
        print("* Have you updated the version?")
        print("* Have you updated CHANGELOG.md?")
        print("* Have you fixed any last minute bugs?")
        print("If you answered yes to all of the above questions,")
        print("then run `invoke release --deploy -vX.YY.ZZ` to:")
        print("- Checkout master")
        print("- Tag the git release with provided vX.YY.ZZ version")
        print("- Push the master branch and tags to repo")
