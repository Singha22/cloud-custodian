# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
from .common import BaseTest


class RAMTest(BaseTest):

    def test_ram_tag(self):
        session_factory = self.replay_flight_data('test_pinpoint_app_tag')


    def test_ram_remove_tag(self):
        session_factory = self.replay_flight_data('test_pinpoint_app_remove_tag')

