import random
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class PostQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)

    def feed(self, user):
        profiles_exists = user.following.exists()
        followed_users_id = []
        if profiles_exists():
            followed_users_id =user.following.values_list("user_id", flat=True) # [x.user.id for x in profiles]
        return self.filter(
            models.Q(user__id__in=followed_users_id) |
            models.Q(user=user)
            ).distinct().order_by("-timestamp")


class PostManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return PostQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)

class Post(models.Model):
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='post_user', blank=True, through=PostLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = PostManager()

    # def __str__(self):
    #     return self.content

    class Meta:
        ordering = ['-id']

    @property
    def is_repost(self):
        return self.parent != None

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'likes': random.randint(0, 200)
        }