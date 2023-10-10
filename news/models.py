from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}'

    def update_rating(self):
        post_rating = self.post_set.all().aggregate(postRating=Sum('rating'))
        p_rate = post_rating.get('postRating')

        comment_rating = self.user.comment_set.all().aggregate(commentRating=Sum('rating'))
        c_rate = comment_rating.get('commentRating')

        post_comment_rating = Comment.objects.filter(post__author=self).aggregate(post_commentRating=Sum('rating'))
        p_c_rate = post_comment_rating.get('post_commentRating')

        self.rating = p_rate * 3 + c_rate + p_c_rate
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    title = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    NEWS = 'NE'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]
    type = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=NEWS,
    )

    rating = models.SmallIntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:123]}…'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    date_joined = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
