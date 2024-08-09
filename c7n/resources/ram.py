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
        arn_type = 'resource-share'
        id = 'resourceShareArns'
        date = 'creationTime'
        enum_spec = ('get_resource_shares', 'resourceShares', None)
        name = 'name'
        permissions = 'ram:GetResourceShares'

    source_mapping = {
        'describe': GetResourceShare
    }
