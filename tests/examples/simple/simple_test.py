#!/usr/bin/env python3

import os

from qatrfm.testcase import TrfmTestCase
from qatrfm.utils.logger import QaTrfmLogger

logger = QaTrfmLogger.getQatrfmLogger(__name__)


class SimpleTest(TrfmTestCase):

    def __init__(self, env, name):
        description = "Example how to transfer files from/to VMs"
        super(SimpleTest, self).__init__(env, name, description)

    def run(self):
        file_to_transfer = (
            "{}/test_file".format(os.path.dirname(os.path.abspath(__file__))))

        vm1 = self.env.domains[0]

        # Transfering a file from a VM
        vm1.transfer_file(remote_file_path='/etc/resolv.conf',
                          local_file_path=self.env.workdir / 'resolv.conf',
                          type='get')
        with open(self.env.workdir / 'resolv.conf', 'r') as f:
            logger.success("Got file: {}".format(f.read()))

        # Transfer file to a VM
        vm1.transfer_file(remote_file_path='/root/test_file',
                          local_file_path=file_to_transfer,
                          type='put')

        # Execute SSH command on a VM
        vm1.execute_ssh_cmd('chmod +x /root/test_file; /root/test_file')

        return self.EX_OK
