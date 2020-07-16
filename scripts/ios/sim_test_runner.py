# Copyright (C) <2020> Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0

'''Script to run tests on iOS simulator.
'''

import os
import sys
import logging
sys.path.append(os.path.join(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..')), 'ios', 'build', 'bots', 'scripts'))
import test_runner

class TestRunner():
    '''
    Encapsulate ios/build/bots/scripts/test_runner.py, call iossim to run tests on simulator.
    '''

    def __init__(self, iossim_path, device_name, ios_ver, out_dir):
        self.iossim_path = iossim_path
        self.ios_ver = ios_ver
        self.device_name = device_name
        self.out_dir = out_dir
        logging.basicConfig(
            format='[%(asctime)s:%(levelname)s] %(message)s',
            level=logging.DEBUG,
            datefmt='%I:%M:%S')

    def run(self, test_app):
        runner = test_runner.SimulatorTestRunner(
            test_app,
            self.iossim_path,
            self.device_name,
            self.ios_ver,
            os.path.join(self.out_dir, os.path.splitext(
                os.path.basename(test_app))[0]),
            env_vars=None,
            retries=None,
            shards=None,
            test_args=None,
            test_cases=None,
            use_clang_coverage=False,
            wpr_tools_path='',
            xctest=None,
        )
        return not runner.launch()
