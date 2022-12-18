from django.utils.html import mark_safe
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from commentator_app.api.mixins import PaginationMixin


class CommentBaseMixin(object):
    serializer_class = None
    model = None


class ListCommentsBaseMixin(CommentBaseMixin, PaginationMixin):
    allowed_orders = ['username', '-username', 'email', '-email', 'created_at', '-created_at']
    default_order = '-created_at'
    queryset = None

    def get_queryset(self):
        return self.queryset

    def get_paginated_data(self, request, view=None):
        return self.paginate_queryset(self.get_queryset(), request, view=view)

    def get_ordering(self):
        order_by = self.request.query_params.get('order_by', self.default_order)
        if order_by not in self.allowed_orders:
            order_by = self.default_order
        return order_by

    def order_queryset(self, queryset):
        return queryset.order_by(self.get_ordering())


class SingleCommentBaseMixin(APIView, CommentBaseMixin):
    lookup_field_type = None
    lookup_field_name = None

    def get_model_lookup_query(self):
        lookup_field = self.kwargs.get(self.lookup_field_name)
        return {self.lookup_field_type: lookup_field}

    def get_object(self):
        return get_object_or_404(self.model, **self.get_model_lookup_query())


class CommentsMixin(APIView, ListCommentsBaseMixin):

    def get_queryset(self):
        return self.order_queryset(self.queryset)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            self.get_paginated_data(request=request, view=self), many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['text'] = mark_safe(data.get('text', ''))
        serializer = self.serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CommentMixin(SingleCommentBaseMixin):
    def get(self, request, *args, **kwargs):
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
