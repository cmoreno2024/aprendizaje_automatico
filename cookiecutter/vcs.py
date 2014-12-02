#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.vcs
----------------

Helper functions for working with version control systems.
"""

from __future__ import unicode_literals
import logging
import os
import subprocess
import sys

from .compat import which
from .exceptions import UnknownRepoType, VCSNotInstalled
from .prompt import query_yes_no
from .utils import make_sure_path_exists, rmtree


def prompt_and_delete_repo(repo_dir, no_input=False):
    """
    Asks the user whether it's okay to delete the previously-cloned repo.
    If yes, deletes it. Otherwise, Cookiecutter exits.

    :param repo_dir: Directory of previously-cloned repo.
    :param no_input: Suppress prompt to delete repo and just delete it.
    """

    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        ok_to_delete = query_yes_no(
            "You've cloned {0} before. "
            'Is it okay to delete and re-clone it?'.format(repo_dir),
            default='yes'
        )

    if ok_to_delete:
        rmtree(repo_dir)
    else:
        sys.exit()


def identify_repo(repo_url):
    """
    Determines if `repo_url` should be treated as a URL to a git or hg repo.

    :param repo_url: Repo URL of unknown type.
    :returns: "git", "hg", or None.
    """

    if 'git' in repo_url:
        return 'git'
    elif 'bitbucket' in repo_url:
        return 'hg'
    else:
        raise UnknownRepoType


def is_vcs_installed(repo_type):
    """
    Check if the version control system for a repo type is installed.

    :param repo_type:
    """
    return bool(which(repo_type))


def clone(repo_url, checkout=None, clone_to_dir=".", no_input=False):
    """
    Clone a repo to the current directory.

    :param repo_url: Repo URL of unknown type.
    :param checkout: The branch, tag or commit ID to checkout after clone.
    :param clone_to_dir: The directory to clone to.
                         Defaults to the current directory.
    :param no_input: Suppress all user prompts when calling via API.
    """

    # Ensure that clone_to_dir exists
    clone_to_dir = os.path.expanduser(clone_to_dir)
    make_sure_path_exists(clone_to_dir)

    # identify the repo_type
    repo_type = identify_repo(repo_url)

    # check that the appropriate VCS for the repo_type is installed
    if not is_vcs_installed(repo_type):
        msg = "'{0}' is not installed.".format(repo_type)
        raise VCSNotInstalled(msg)

    tail = os.path.split(repo_url)[1]
    if repo_type == 'git':
        repo_dir = os.path.normpath(os.path.join(clone_to_dir,
                                                 tail.rsplit('.git')[0]))
    elif repo_type == 'hg':
        repo_dir = os.path.normpath(os.path.join(clone_to_dir, tail))
    logging.debug('repo_dir is {0}'.format(repo_dir))

    if os.path.isdir(repo_dir):
        prompt_and_delete_repo(repo_dir, no_input=no_input)

    if repo_type in ['git', 'hg']:
        try:
            # if you don't use check_output, you get it on stderr no matter;
            #  - might as well use check_output, and choose your control:
            # subprocess.check_call([repo_type, 'clone', repo_url], cwd=clone_to_dir)
            ## check_output for git doesn't seem to ever return anything insightful;
            ret = subprocess.check_output([repo_type, 'clone', repo_url], cwd=clone_to_dir, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            print "Error: the following failed (returned {d}):\n  {s}" \
                  .format(d=e.returncode, s=' '.join(e.cmd))
            ## only captured in check_output calls:
            #print "  {s}".format(s="\n  ".join(e.output.splitlines()))
            sys.exit(-1)
        if checkout is not None:
            subprocess.check_call([repo_type, 'checkout', checkout],
                                  cwd=repo_dir)

    return repo_dir
