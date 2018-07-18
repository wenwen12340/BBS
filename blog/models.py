from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=64,verbose_name='个人博客标题')
    site_name = models.CharField(max_length=64,verbose_name='站点名称')
    theme = models.CharField(max_length=64,verbose_name='博客主题')

    #站点表，和userinfo是一对一关系,在此表中建立关联字段
    def __str__(self):
        return self.title

class Userinfo(AbstractUser):

    tel = models.CharField(max_length=11,unique=True,null=True)
    avatar = models.FileField(upload_to='avatars/',default='avatars/touxiang.png')
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    blog = models.OneToOneField(to="Blog",to_field ='id',null=True,on_delete=models.CASCADE)


    def __str__(self):
        return self.username

class Artical(models.Model):
    title = models.CharField(max_length=32,verbose_name='文章标题')
    abstract = models.CharField(max_length=225,verbose_name='文章描述')
    content = models.TextField()
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    #和userinfo是多对一的关系，在此表中建立关联按字段
    user = models.ForeignKey(to='Userinfo', to_field='id', on_delete=models.CASCADE)
    #和category是多对一的关系，在此表中建立关联按字段
    category= models.ForeignKey(to='Category', to_field='id', on_delete=models.CASCADE)
    #和tag是多对多的关系，在此表中建立关联按字段，生成artical_tag表
    tags = models.ManyToManyField(to='Tag',through='Artical2Tag')

class Artical2Tag(models.Model):
    artical = models.ForeignKey(to='Artical',to_field='id',on_delete=models.CASCADE)
    tag = models.ForeignKey(to='Tag',to_field='id',on_delete=models.CASCADE)


    def __str__(self):
        v = self.artical.title + '___' + self.tag.title
        return v

class Aritalupdown(models.Model):
    is_up = models.BooleanField(default=True)
    # 和userinfo是多对一的关系，在此表中建立管理按字段
    user = models.ForeignKey(to='Userinfo',to_field='id',on_delete=models.CASCADE)
    #和artical是多对一的关系，在此表中建立管理按字段
    artical = models.ForeignKey(to='Artical',to_field='id',on_delete=models.CASCADE)

    # class Meta:
    #     unique_together = [
    #         ('artical', 'user')
    #     ]

class Comment(models.Model):
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    #和userinfo是多对一的关系，在此表中建立管理按字段
    user = models.ForeignKey(verbose_name='评论者',to='Userinfo', to_field='id', on_delete=models.CASCADE)
    #和artical是多对一的关系，在此表中建立管理按字段
    artical = models.ForeignKey(verbose_name='评论文章',to='Artical',to_field='id',on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(to='Comment',to_field='id',on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.content

class Tag(models.Model):
    #和artical是多对多关系
    title= models.CharField(max_length=32,verbose_name='标签名称')
    #和Blog是多对一的关系
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='id',on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=32,verbose_name='分类标题')
    #和Blog是多对一的关系
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='id',on_delete=models.CASCADE)

    def __str__(self):
        return  self.title
    #和artical是一对多关系



