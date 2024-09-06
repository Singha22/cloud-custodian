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
