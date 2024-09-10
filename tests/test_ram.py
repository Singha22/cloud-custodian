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
        print("resoruces", resources)
        self.assertEqual(len(resources), 1)
        tags = client.get_resource_shares(resourceOwner="SELF")["resourceShares"][0]["tags"]
        print("tags", tags)
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags, [{'key': 'resource', 'value': 'agent'}])

    def test_delete_ram_resource_share(self):
        session_factory = self.replay_flight_data("test_delete_ram_resource_share")
        p = self.load_policy(
            {
                "name": "ram-resource-share-delete",
                "resource": "ram-resource-share",
                "filters": [{"tag:owner": "policy"}],
                "actions": [{
                    "type": "delete",
                }],
            },
            session_factory=session_factory,
        )
        resources = p.run()
        self.assertEqual(1, len(resources))
        client = session_factory().client('ram')
        resource_shares = client.get_resource_shares(resourceOwner="SELF")['resourceShares']

        for resource in resource_shares:
            if resource['resourceShareArn'] == resources[0]['resourceShareArn']:
                self.assertEqual(resource['status'], 'DELETED')
                break
        else:
            self.fail(f"Resource share {resources[0]['resourceShareArn']} failed")
