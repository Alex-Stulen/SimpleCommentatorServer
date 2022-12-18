from rest_framework.permissions import AllowAny

from commentator_app import models
from . import serializers
from . import mixins


class CommentsAPIView(mixins.CommentsMixin):
    serializer_class = serializers.CommentSerializer
    permission_classes = (AllowAny, )

    model = models.Comment
    queryset = model.objects.all_main_comments()


class CommentAPIView(mixins.CommentMixin):
    serializer_class = serializers.CommentSerializer
    permission_classes = (AllowAny, )

    model = models.Comment
    lookup_field_type = 'pk'
    lookup_field_name = 'comment_id'


class CommentRepliesAPIView(mixins.CommentRelativeListMixin):
    serializer_class = serializers.CommentSerializer
    permission_classes = (AllowAny, )

    model = models.Comment
    lookup_field_type = 'pk'
    lookup_field_name = 'comment_id'

    def get_queryset(self):
        return self.order_queryset(self.model.objects.replies_all(instance=self.get_object()))
