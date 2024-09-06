from c7n.actions import ActionRegistry
from c7n.filters import FilterRegistry
from c7n.manager import resources
from c7n.query import QueryResourceManager, TypeInfo, DescribeSource
from c7n.tags import universal_augment, Tag, RemoveTag


class GetResourceShare(DescribeSource):
    def augment(self, resources):
        return universal_augment(self.manager, super().augment(resources))


filters = FilterRegistry('ram.filters')
actions = ActionRegistry('ram.actions')


@resources.register('ram')
class RAM(QueryResourceManager):
    class resource_type(TypeInfo):
        service = 'ram'
        filter_name = 'resourceShareArns'
        filter_type = list
        arn_type = 'resource-share'
        id = name = 'resourceShareArn'
        enum_spec = ('get_resource_shares', 'resourceShares', {"resourceOwner": "SELF"})
        permissions = 'ram:GetResourceShares'
        universal_taggable = True

    source_mapping = {
        'describe': GetResourceShare
    }

    filter_registry = filters
    action_registry = actions


@RAM.action_registry.register('tag')
class TagRAM(Tag):
    """Creates tags on the RAM

    :example:

    .. code-block:: yaml

        policies:
            - name: ram-tag
              resource: aws.ram
              actions:
                - type: tag
                  key: test
                  value: something
    """
    permissions = ('ram:TagResource', 'ram:GetResourceShares')

    def process_resource_set(self, client, resources, new_tags):
        tags = [{'key': item['Key'], 'value': item['Value']} for item in new_tags]
        for r in resources:
            client.tag_resource(resourceShareArn=r["resourceShareArn"], tags=tags)


@RAM.action_registry.register('remove-tag')
class RemoveTagRAM(RemoveTag):
    """Removes tags on the RAM

    :example:

    .. code-block:: yaml
        policies:
            - name: ram-untag
              resource: aws.ram
              actions:
                - type: remove-tag
                  tags: ["tag-key"]
    """
    permissions = ('ram:UntagResource', 'ram:GetResourceShares')

    def process_resource_set(self, client, resources, tags):
        for r in resources:
            client.untag_resource(resourceShareArn=r["resourceShareArn"], tagKeys=tags)
