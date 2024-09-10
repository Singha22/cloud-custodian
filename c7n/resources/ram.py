from c7n.actions import BaseAction
from c7n.manager import resources
from c7n.query import QueryResourceManager, TypeInfo
from c7n.tags import universal_augment
from c7n.utils import type_schema, local_session


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

    augment = universal_augment


@RAMResourceShare.action_registry.register('delete')
class DeleteResourceShare(BaseAction):
    """
    Deletes an AWS RAM resource share based on certain filter criteria.

    :example:

    .. code-block:: yaml

        policies:
          - name: ram-resource-share-delete
            resource: ram-resource-share
            actions:
              - type: delete
    """

    schema = type_schema('delete')
    permissions = ('ram:DeleteResourceShare',)

    def process(self, resources):
        client = local_session(self.manager.session_factory).client('ram')

        for r in resources:
            resource_share_arn = r['resourceShareArn']
            self.manager.log.info(f"Deleting resource share: {resource_share_arn}")
            try:
                client.delete_resource_share(
                    resourceShareArn=resource_share_arn
                )
            except Exception as e:
                self.manager.log.error(f"An error occurred when deleting resource share "
                                       f"{resource_share_arn}: {str(e)}")
