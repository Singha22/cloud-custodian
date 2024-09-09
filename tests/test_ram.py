# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
from .common import BaseTest


class RAMTest(BaseTest):

    def test_ram_tag_untag_resource(self):
        session_factory = self.replay_flight_data('test_ram_tag_untag_resource')
        client = session_factory().client('ram')
        p = self.load_policy({
            'name': 'ram-tag',
            'resource': 'ram-resource-share',
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

        }, session_factory=session_factory)
        resources = p.run()
        print("resources are", resources)
        self.assertEqual(len(resources), 1)
        tags = client.get_resource_shares(resourceOwner="SELF")["resourceShares"][0]["tags"]
        self.assertEqual(len(tags), 1)
        # self.assertEqual(tags, [{'key': 'resource', 'value': 'agent'}])
