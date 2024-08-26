from c7n.manager import resources
from c7n.query import QueryResourceManager, TypeInfo, DescribeSource
from c7n.tags import universal_augment


class GetResourceShare(DescribeSource):
    def augment(self, resources):
        return universal_augment(self.manager, super().augment(resources))


@resources.register('ram')
class RAM(QueryResourceManager):
    class resource_type(TypeInfo):
        service = 'ram'
        filter_name = 'resourceShareArns'
        filter_type = list
        arn_type = 'resource-share'
        id = name = 'resourceShareArns'
        enum_spec = ('get_resource_shares', 'resourceShareArns', {"resourceOwner": "SELF"})
        permissions = 'ram:GetResourceShares'
        universal_taggable = object()

    source_mapping = {
        'describe': GetResourceShare
    }
