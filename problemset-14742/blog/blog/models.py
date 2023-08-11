from django.db import models
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=50)


class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    def copy(self):
        new_post = BlogPost.objects.create(title=self.title,
                                           body=self.body,
                                           author=self.author,
                                           date_created=timezone.now()
                                           )
        comments = self.comments.all()
        for comment in comments:
            Comment.objects.create(blog_post=new_post, text=comment.text)
        return new_post.id


class Comment(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
