from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=200)  # заголовок
    author = models.ForeignKey(  # автор (отношение многие-к-одному)
        "auth.User",
        on_delete=models.CASCADE,
    )
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    author = models.ForeignKey(  # автор (отношение многие-к-одному)
        "auth.User",
        on_delete=models.CASCADE,
        default=User.objects.first().pk
    )
    post = models.ForeignKey(Post, related_name='comments', default=Post.objects.first().pk, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    body = models.TextField()

    def __str__(self):
        return 'Comment by {} on {}'.format(self.title, self.post)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.post.pk})
