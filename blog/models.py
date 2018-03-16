import datetime
import markdown

from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings


class Post( models.Model ):
    author = models.ForeignKey('auth.User')
    title = models.CharField( max_length=200 )
    body = models.TextField()
    images = models.ManyToManyField( Image, blank=True )
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def body_html( self ):
        return markdown_to_html( self.body, self.images.all() )

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
    
    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text

def markdown_to_html( markdownText, images ):
    image_ref = ""
    
    for image in images:
        image_url = settings.MEDIA_URL + image.image.url
        image_ref = "%s\n[%s]: %s" % ( image_ref, image, image_url )

    md = "%s\n%s" % ( markdownText, image_ref )
    html = markdown.markdown( md )

    return html

class Image( models.Model ):
    name = models.CharField( max_length=100 )
    image = models.ImageField( upload_to="image" )
    
    def __unicode__( self ):
        return self.name
