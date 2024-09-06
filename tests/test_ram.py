# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
from .common import BaseTest


class RAMTest(BaseTest):

    def test_ram_tag_untag_resource(self):
        factory = self.replay_flight_data('test_ram_tags')
        p = self.load_policy({
            'name': 'ram-tags',
            'resource': 'ram',
            'filters': [
                {
                    'tag:resource': 'absent'
                },
                {
                    'tag:owner': 'policy'
                }
            ],
            'actions': [
                {
                    "type": "tag",
                    "tags": {"resource": "agent"}
                },
                {
                    "type": "remove-tag",
                    "tags": ["owner"]
                }
            ]

        }, session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        client = factory().client('ram')
        tags = client.get_resource_shares(resourceOwner="SELF")["resourceShares"][0]["tags"]
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags, [{'key': 'resource', 'value': 'agent'}])
