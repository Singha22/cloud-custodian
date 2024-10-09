# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
from .common import BaseTest


class WAFTest(BaseTest):

    def test_waf_query(self):
        session_factory = self.replay_flight_data("test_waf_query")
        p = self.load_policy(
            {"name": "waftest", "resource": "waf"}, session_factory=session_factory
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(
            resources[0]["WebACLId"], "1ebe0b46-0fd2-4e07-a74c-27bf25adc0bf"
        )
        self.assertEqual(resources[0]["DefaultAction"], {"Type": "BLOCK"})

    def test_wafv2_resolve_resources(self):
        session_factory = self.replay_flight_data(
            "test_wafv2_resolve_resources",
            region="us-east-2"
        )
        p = self.load_policy(
            {"name": "wafv2test", "resource": "aws.wafv2"},
            session_factory=session_factory,
            config={"region": "us-east-2"}
        )
        resources = p.resource_manager.get_resources(["624e04d2-8b45-45ee-b4ad-e853dac6d070"])
        assert len(resources) == 1

    def test_wafv2_logging_configuration(self):
        session_factory = self.replay_flight_data(
            'test_wafv2_logging_configuration')
        policy = {
            'name': 'foo',
            'resource': 'aws.wafv2',
            'filters': [
                {
                    'type': 'logging',
                    'key': 'RedactedFields[].SingleHeader.Name',
                    'value': 'user-agent',
                    'value_type': 'swap',
                    'op': 'in'
                }
            ]
        }
        p = self.load_policy(
            policy,
            session_factory=session_factory,
            config={'region': 'us-east-1'}
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertTrue('c7n:WafV2LoggingConfiguration' in resources[0])
        self.assertEqual(
            resources[0]['c7n:WafV2LoggingConfiguration']['RedactedFields'],
            [
                {
                    'SingleHeader': {
                        'Name': 'user-agent'
                    }
                }
            ]
        )

    def test_wafv2_logging_not_enabled(self):
        session_factory = self.replay_flight_data(
            'test_wafv2_no_logging_configuration')
        policy = {
            'name': 'foo',
            'resource': 'aws.wafv2',
            'filters': [
                {
                    'not': [{
                        'type': 'logging',
                        'key': 'ResourceArn',
                        'value': 'present'
                    }]
                }
            ]
        }
        p = self.load_policy(
            policy,
            session_factory=session_factory,
            config={'region': 'us-east-1'}
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertTrue('c7n:WafV2LoggingConfiguration' not in resources[0])

    def test_wafv2_enable_logging(self):
        session_factory = self.replay_flight_data("test_wafv2_enable_logging")
        policy = {
            "name": "wafv2-enable-logging",
            "resource": "aws.wafv2",
            "filters": [
                {
                    "type": "value",
                    "key": "Name",
                    "value": "test-custodian-waf",
                    "op": "eq"
                }
            ],
            "actions": [
                {
                    "type": "enable-logging",
                    "log_destination_arn": "arn:aws:s3:::aws-waf-logs-test-custodian-creation"
                }
            ]
        }
        p = self.load_policy(policy,
                             session_factory=session_factory,
                             config={"region": "us-east-1"})

        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]["ARN"],
                         "arn:aws:wafv2:us-east-1:644160558196:regional/webacl/test-custodian-waf/0b6d34b1-689c-4d33-8d84-3effe427413f")

        client = session_factory().client("wafv2")
        logging_config = client.get_logging_configuration(ResourceArn=resources[0]["ARN"])
        self.assertEqual(logging_config["LoggingConfiguration"]["ResourceArn"], resources[0]["ARN"])
        self.assertEqual(logging_config["LoggingConfiguration"]["LogDestinationConfigs"][0],
                         "arn:aws:s3:::aws-waf-logs-test-custodian-creation")
