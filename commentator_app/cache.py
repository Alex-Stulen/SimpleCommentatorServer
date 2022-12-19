import json

from django.conf import settings

import redis


class CommentsRedisManager:
    COMMENTATOR_CLUSTER = 'simple_commentator'
    COMMENTS_CLUSTER = 'comments'

    def __init__(self, host, port, db, *args, **kwargs):
        self.client = redis.Redis(host=host, port=port, db=db, *args, **kwargs)
        self.setup()

    def setup(self):
        self.client.set(self.COMMENTATOR_CLUSTER, json.dumps({self.COMMENTS_CLUSTER: {}}))
        self.client.set(self.COMMENTS_CLUSTER, json.dumps({}))

    def get_commentator_cluster(self) -> dict:
        cluster = self.client.get(self.COMMENTATOR_CLUSTER)
        return json.loads(cluster.decode())

    def get_comments_cluster(self) -> dict:
        commentator_cluster = self.get_commentator_cluster()
        comments_cluster: dict = commentator_cluster.get(self.COMMENTS_CLUSTER, {})
        return comments_cluster

    def set_comments_cluster(self, new_cluster: dict):
        commentator_cluster = self.get_commentator_cluster()
        commentator_cluster[self.COMMENTS_CLUSTER] = new_cluster
        self.client.set(self.COMMENTATOR_CLUSTER, json.dumps(commentator_cluster))
        return new_cluster

    def set_comment(self, comment_id: int, comment_data: dict):
        comments_cluster = self.get_comments_cluster()
        comments_cluster[comment_id] = comment_data
        self.set_comments_cluster(comments_cluster)
        return comments_cluster

    def get_comment(self, comment_id):
        return self.get_comments_cluster().get(str(comment_id))

    def get_comments_list(self):
        return list(self.get_comments_cluster().values())


comments_redis_manager = CommentsRedisManager(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DATABASE)
