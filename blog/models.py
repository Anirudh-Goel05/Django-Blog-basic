from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey("auth.User",on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.title
    def get_comments(self):
        return Comment.objects.filter(post=self)
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def approved_comments(self):
        return self.comments.filter(is_approved=True)
    def get_absolute_url(self):
        return reverse('blog:post_detail',kwargs={'pk':self.pk})

class Comment(models.Model):
    post = models.ForeignKey('Post',related_name='comments',on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    is_approved = models.BooleanField(default=False)

    def approve_comment(self):
        if self.is_approved == False:
            self.is_approved = True
    def get_absolute_url(self):
        return reverse('blog:posts_list')

    def __str__(self):
        return self.text
