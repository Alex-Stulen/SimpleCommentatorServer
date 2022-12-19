from django.utils.html import mark_safe
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from commentator_app.api.mixins import PaginationMixin
from commentator_app import cache


class CommentBaseMixin(object):
    serializer_class = None
    model = None


class ListCommentsBaseMixin(CommentBaseMixin, PaginationMixin):
    allowed_orders = ['username', '-username', 'email', '-email', 'created_at', '-created_at']
    default_order = '-created_at'
    query_ordering_name = 'order_by'
    queryset = None

    def get_queryset(self):
        return self.queryset

    def get_paginated_data(self, request, queryset=None, view=None):
        queryset = queryset if queryset else self.get_queryset()
        return self.paginate_queryset(queryset, request, view=view)

    def get_ordering(self, remove_minus_prefix=False):
        order_by = self.request.query_params.get(self.query_ordering_name, self.default_order)

        if order_by not in self.allowed_orders:
            order_by = self.default_order

        if remove_minus_prefix and self.is_reverse_ordering():
            order_by = order_by[1:]

        return order_by

    def is_reverse_ordering(self):
        return self.get_ordering().startswith('-')

    def order_queryset(self, queryset):
        return queryset.order_by(self.get_ordering())

    def order_list(self, list_, key=None, reverse=None):
        if key is None:
            order_by = self.get_ordering(remove_minus_prefix=self.is_reverse_ordering())
            key = lambda el: el[order_by]

        if reverse is None:
            reverse = self.is_reverse_ordering()

        return sorted(list_, key=key, reverse=reverse)


class SingleCommentBaseMixin(APIView, CommentBaseMixin):
    lookup_field_type = None
    lookup_field_name = None

    def get_model_lookup_query(self):
        lookup_field = self.kwargs.get(self.lookup_field_name)
        return {self.lookup_field_type: lookup_field}

    def get_object(self):
        return get_object_or_404(self.model, **self.get_model_lookup_query())


class CommentsMixin(APIView, ListCommentsBaseMixin):
    cache_manager = cache.comments_redis_manager

    def get_cache_list(self):
        return self.cache_manager.get_comments_list()

    def to_cache(self, comment):
        comment_json = self.serializer_class(instance=comment).data
        self.cache_manager.set_comment(comment.pk, comment_json)
        return comment_json

    def cache_queryset(self, queryset):
        for comment in queryset:
            self.to_cache(comment)
        return queryset

    def get_queryset(self):
        cache_list = self.get_cache_list()
        # check cache list
        if not cache_list:
            queryset = self.order_queryset(self.queryset)
            # write to cache
            queryset = self.cache_queryset(queryset)
            return queryset
        return self.order_list(cache_list)

    def get(self, request, *args, **kwargs):
        # check cache list
        if not self.get_cache_list():
            serializer = self.serializer_class(
                self.get_paginated_data(request=request, view=self), many=True)
            return self.get_paginated_response(serializer.data)
        else:
            # return from cache
            paginated_list = self.get_paginated_data(request, self.get_queryset(), view=self)
            return self.get_paginated_response(paginated_list)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['text'] = mark_safe(data.get('text', ''))
        serializer = self.serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CommentMixin(SingleCommentBaseMixin):
    cache_manager = cache.comments_redis_manager

    def get_cache_data(self):
        comment_id = self.get_model_lookup_query().get('pk', None)
        return self.cache_manager.get_comment(comment_id)

    def get(self, request, *args, **kwargs):
        cache_data = self.get_cache_data()
        if not cache_data:
            return Response(cache_data)

        obj = self.get_object()
        serializer = self.serializer_class(instance=obj)
        return Response(serializer.data)


class CommentRelativeListMixin(ListCommentsBaseMixin, SingleCommentBaseMixin):

    def get_queryset(self):
        return self.order_queryset(self.queryset)

    def get_object(self):
        return get_object_or_404(self.model, **self.get_model_lookup_query())

    def get(self, request, *args, **kwargs):
        paginated_data = self.paginate_queryset(self.get_queryset(), request, view=self)
        serializer = self.serializer_class(paginated_data, many=True)
        return self.get_paginated_response(serializer.data)
