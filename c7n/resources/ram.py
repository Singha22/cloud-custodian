from c7n.manager import resources
from c7n.query import QueryResourceManager, TypeInfo, DescribeSource
from c7n.tags import universal_augment


class GetResourceShare(DescribeSource):
    def augment(self, resources):
        return universal_augment(self.manager, super().augment(resources))


@resources.register('ram-resource-share')
class RAMResourceShare(QueryResourceManager):
    class resource_type(TypeInfo):
        service = 'ram'
        enum_spec = ('get_resource_shares', 'resourceShares', {"resourceOwner": "SELF"})
        filter_type = list
        filter_name = 'resourceShareArns'
        arn_type = 'resource-share'
        id = name = 'resourceShareArn'
        permissions = 'ram:GetResourceShares'
        universal_taggable = object()

    source_mapping = {
        'describe': GetResourceShare
    }
