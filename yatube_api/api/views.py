from sqlite3 import IntegrityError

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import mixins, pagination
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, \
    IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, \
    GenericViewSet

from posts.models import Group, Post, Comment, Follow
from .permissions import IsAuthorOrReadOnly
from .serializers import GroupSerializer, PostSerializer, CommentSerializer, \
    FollowSerializer


# Create your views here.
class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_post(self):
        if not hasattr(self, 'calculated_post'):
            post_id = self.kwargs['post_id']
            self.calculated_post = get_object_or_404(Post, pk=post_id)
        return self.calculated_post

    def filter_queryset(self, queryset):
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, ]

    def filter_queryset(self, queryset):
        queryset = queryset.filter(user=self.request.user)
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(following__username=search)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                raise ValidationError(
                    {'detail': 'This entry violates a unique constraint.'})
            raise e
        except Exception as e2:
            raise e2
