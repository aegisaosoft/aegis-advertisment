# -*- coding: utf-8 -*-
"""No script in this folder carries a credential in its source.

The capture scripts sign in to the sandbox with a test account; its password lives in the environment
(TUTORIAL_SANDBOX_PASSWORD) or the gitignored _sandbox_password.txt, never in a committed file.
"""
import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
# A password written as a literal: `password: '...'` or `password = "..."`.
LITERAL = re.compile(r"""password\s*[:=]\s*(['"])[^'"]+\1""", re.I)


def test_no_script_has_a_literal_password():
    offenders = []
    for path in glob.glob(os.path.join(HERE, '*.js')) + glob.glob(os.path.join(HERE, '*.py')):
        if os.path.basename(path) == os.path.basename(__file__):
            continue                                    # its own pattern, in the comment above
        for n, line in enumerate(open(path, encoding='utf-8', errors='replace'), 1):
            if LITERAL.search(line):
                offenders.append('%s:%d' % (os.path.basename(path), n))
    assert offenders == []


def test_the_capture_scripts_read_the_password_from_outside_git():
    for name in ('capture-register.js', 'stripe-walk.js'):
        src = open(os.path.join(HERE, name), encoding='utf-8').read()
        assert 'password: sandboxPassword()' in src
        assert 'TUTORIAL_SANDBOX_PASSWORD' in src
