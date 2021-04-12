# Copyright (C) <2021> Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0

'''Script to roll owt-deps-webrtc revision.

This script is expected to run by GitHub action runners when a new change is
committed to owt-deps-webrtc. It updates the revision in DEPS to use the latest
owt-deps-webrtc. A change will be submitted to owt-client-native's
auto-rollers/webrtc branch. And a pull request will be opened if it doesn't
exist.
'''

import os
import sys
import argparse
import re
import subprocess
import requests

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEPS_PATH = os.path.join(SRC_PATH, 'DEPS')
# Regex expression to match commit hash of owt-deps-webrtc.
REVISION_RE = re.compile(
    r"(?<=Var\('deps_webrtc_git'\) \+ '/owt-deps-webrtc' \+ '@' \+ ')[0-9a-f]{40}(?=',)")


def webrtc_revision():
    '''Return current owt-deps-webrtc revision in DEPS.'''
    with open(DEPS_PATH, 'r') as f:
        deps = f.read()
        return re.search(REVISION_RE, deps).group(0)


def roll(revision):
    with open(DEPS_PATH, 'r+') as f:
        deps = f.read()
        new_deps = re.sub(REVISION_RE, revision, deps)
        f.seek(0)
        f.truncate()
        f.write(new_deps)
    return


def commit_message(old_revision, new_revision):
    message = 'Roll WebRTC revision %s..%s.' % (
        old_revision[:8], new_revision[:8])
    return message


def commit(old_revision, new_revision):
    message = commit_message(old_revision, new_revision)
    # Create a git commit with message above.
    subprocess.call(['git', 'add', 'DEPS'], cwd=SRC_PATH)
    subprocess.call(['git', 'commit', '-m', message], cwd=SRC_PATH)
    # Force push because when a new version of owt-deps-webrtc is available, the old commit could be rewritten.
    subprocess.call(['git', 'push', '-f', 'https://github.com/open-webrtc-toolkit/owt-client-native.git',
                     'HEAD:refs/heads/auto-rollers/webrtc'])


def pr(old_revision, new_revision):
    '''Create a pull request. If a PR is already open for webrtc roller, do nothing.'''
    # Check if a pull request exists.


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--revision', help='owt-deps-webrtc revision to roll to.')
    opts = parser.parse_args()
    old_revision = webrtc_revision()
    roll(opts.revision)
    commit(old_revision, opts.revision)
    return 0


if __name__ == '__main__':
    sys.exit(main())
