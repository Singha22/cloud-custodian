# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
from .common import BaseTest


class RAMTest(BaseTest):

    def test_ram_tag_resource(self):
        factory = self.replay_flight_data('test_ram_tags')
        p = self.load_policy({
            'name': 'ram-tags',
            'resource': 'ram',
            'filters': [
                {
                    'tag:Category': 'absent'
                }
            ],

        }, session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_ram_untag_resource(self):
        factory = self.replay_flight_data('test_ram_untag_resource')
        p = self.load_policy({
            'name': 'ram-remove-tag',
            'resource': 'ram',
            'filters': [
                {
                    'tag:Category': 'absent'
                }
            ],
            'actions': ['remove-tag'],
        }, session_factory=factory)
        resources = p.run()

        self.assertEqual(len(resources), 1)
