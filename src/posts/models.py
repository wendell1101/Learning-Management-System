from django.db import models
from django.contrib.auth.models import User
from crud.models import ClassName
class Post(models.Model):
    classname = models.ForeignKey(ClassName,on_delete=models.CASCADE, default='')   
    content = models.TextField(verbose_name="")
    date_posted = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User,on_delete = models.CASCADE)
    attachment = models.FileField(upload_to="file_attachments/", default = '',blank=True)
    image = models.ImageField(upload_to="image_attachments/",default='',blank=True)
    def __str__(self):
        return self.content
