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
        self.assertEqual(len(resources), 1)
        tags = client.get_resource_shares(resourceOwner="SELF")["resourceShares"][0]["tags"]
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

    def test_ram_mark_for_op_resource_share(self):
        session_factory = self.replay_flight_data('test_ram_mark_for_op_resource_share')
        client = session_factory().client('ram')
        p = self.load_policy({
            'name': 'ram-mark-for-op',
            'resource': 'ram-resource-share',
            'filters': [
                {
                    'tag:owner': 'policy',
                }
            ],
            'actions': [
                {
                    'type': 'mark-for-op',
                    'tag': 'custodian_cleanup',
                    'op': 'delete',
                    'days': 7
                }
            ]
        }, session_factory=session_factory)

        resources = p.run()
        self.assertEqual(1, len(resources))
        tags = client.get_resource_shares(resourceOwner="SELF")['resourceShares'][0]['tags']
        self.assertEqual(len(tags), 2)
        self.assertEqual(tags, [
            {
                'key': 'owner',
                'value': "policy"
            },
            {
                'key': 'custodian_cleanup',
                'value': "Resource does not meet policy: delete@2024/09/18"
            }
            ]
        )
    #
    # def test_ram_marked_for_op_resource_share(self):
    #     session_factory = self.replay_flight_data('test_ram_marked_for_op_resource_share')
    #     p = self.load_policy({
    #         'name': 'ram-marked-for-op',
    #         'resource': 'ram-resource-share',
    #         'filters': [
    #             {
    #                 'type': 'marked-for-op',
    #                 'tag': 'custodian_cleanup',
    #                 'op': 'delete',
    #                 'skew': 1
    #             }
    #         ],
    #         'actions': [
    #             {
    #                 'type': 'delete'
    #             }
    #         ]
    #     }, session_factory=session_factory)
    #
    #     resources = p.run()
    #     self.assertEqual(len(resources), 1)
    #     client = session_factory().client('ram')
    #     resource_shares = client.get_resource_shares(resourceOwner="SELF")['resourceShares']
    #
    #     for resource in resource_shares:
    #         if resource['resourceShareArn'] == resources[0]['resourceShareArn']:
    #             self.assertEqual(resource['status'], 'DELETED')
    #             break
    #     else:
    #         self.fail(f"Resource share {resources[0]['resourceShareArn']} "
    #                   f"was not deleted")
