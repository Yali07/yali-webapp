from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image

# Create your models here.

class BlogPost(models.Model):
    title = models.CharField(default='<Untitled>',null=True,blank=True,max_length=200)
    slug = models.SlugField(blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    category = models.CharField(max_length=108,null=True,blank=True)
    body = RichTextUploadingField(null=True)
    snippet = models.CharField(max_length=200,blank=True,null=True)
    snippet_image= models.ImageField(blank=True,null=True,upload_to='snippet_pics')
    def __str__(self):
    	return self.title
    def save(self, *args,**kwargs):
        self.slug = slugify(self.title)
        super().save(*args,**kwargs)
        
        # img = Image.open(self.snippet_image.path)
        # if img.height > 250 or img.width > 250:
        #     output_size = (250,250)
        #     img.thumbnail(output_size)
        #     img.save(self.snippet_image.path)
        
        
    def get_absolute_url(self):
    	return f"/{self.slug}"      
        
class Comment (models.Model):

    post = models.ForeignKey(BlogPost,related_name='comments',on_delete=models.CASCADE)
    user = models.ForeignKey(User,editable=False, on_delete=models.CASCADE)
    date_added =  models.DateTimeField(auto_now_add=True,null=True)
    comment = models.TextField(null=True)

    def __str__(self):
        return '%s - %s' % (self.comment,self.user.username) 
    
class Category(models.Model):
    category_name = models.CharField(max_length=108,null=True,blank=True)

    def __str__(self):
        return self.category_name
class Subscribe(models.Model):
    subscribers = models.CharField(max_length=108,null=True)
    def __str__(self):
        return self.subscribers
class NewsLetter(models.Model):
    subject = models.CharField(max_length=250,null=True,blank=True)
    email_pics= models.ImageField(upload_to='email_pics',null=True,blank=True)
    message = RichTextUploadingField(null=True)


