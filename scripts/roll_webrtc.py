# Copyright (C) <2021> Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0

'''Script to roll owt-deps-webrtc revision.
'''

import os
import sys
import argparse
import re

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


def commit(old_revision, new_revision):
    message = 'Roll WebRTC revision %s..%s.' % (
        old_revision[:8], new_revision[:8])
    # Create a git commit with message above.


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
