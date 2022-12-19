from django.db.models.signals import post_save
from django.dispatch import receiver

from commentator_app import models
from commentator_app.cache import comments_redis_manager
from commentator_app.api.v1.serializers import CommentSerializer


@receiver(post_save, sender=models.Comment)
def update_comment_cache(sender, instance, **kwargs):
    print('start update_comment_cache')
    instance_json = CommentSerializer(instance=instance).data
    comments_redis_manager.set_comment(instance.pk, instance_json)
    print(comments_redis_manager.get_comments_cluster())
