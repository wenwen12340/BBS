from django.shortcuts import render,HttpResponse,reverse,redirect
from django.contrib import auth
from blog.models import Artical,Userinfo,Blog,Category,Tag,Aritalupdown,Comment,Artical2Tag
from django.db.models import Count
from bs4 import BeautifulSoup
from utils.code import check_code
# Create your views here.
def code(request):
    img,random_code = check_code()
    request.session['random_code'] = random_code
    from io import BytesIO
    stream = BytesIO()
    img.save(stream,'png')
    return HttpResponse(stream.getvalue())


def login(request):
    if request.method =='GET':
        return render(request,'login.html')
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    code = request.POST.get('code')
    if code.upper() != request.session['random_code'].upper():
        return render(request, 'login.html', {'msg': '验证码错误'})
    user = auth.authenticate(username=user,password=pwd)
    if user:
        auth.login(request,user)
        reverse('index')
        return redirect('index')
    return render(request,'login.html',{'msg': '用户名或密码错误'})

def logout(request):
    auth.logout(request)
    print(request.user.username)
    reverse('index')
    return redirect('index')


def index(request):
    artical_list = Artical.objects.all()

    return render(request,'index.html',{'artical_list':artical_list})

def site(request,username,**kwargs):
    user = Userinfo.objects.filter(username=username).all().first()
    # print(user)
    if not user:
        reverse('index')
        redirect('index')

    blog= user.blog
    if not kwargs:
        artical_list= Artical.objects.filter(user__username=username).all()
    else:
        condition = kwargs.get('condition')
        params= kwargs.get('params')
        if condition=='category':
            artical_list = Artical.objects.filter(user__username=username).filter(category__title=params)
        elif condition == 'tag':
            artical_list = Artical.objects.filter(user__username=username).filter(tags__title=params)
        else:
            year,month = params.split('/')
            print(year,month)
            # year = str(year)
            # month = str(month)
            artical_list=Artical.objects.filter(user__username=username).filter(create_time__year=year,create_time__month=month)
            print(artical_list)

    if not artical_list:
        reverse('index')
        redirect('index')

    # category_list = Category.objects.filter(blog=blog,artical__user__username=user.username).annotate(c=Count('artical__title')).values_list('title','c')
    # print(category_list)
    #
    # tag_list = Tag.objects.filter(blog=blog,artical__user__username=user.username).annotate(c=Count('artical__title')).values_list('title','c')
    # print(tag_list)
    #
    # artical_list = Artical.objects.filter(user__username=username).all()
    # print(artical_list)
    #
    # date_list = Artical.objects.filter(user=user).extra(select={'y_m_date':'DATE_FORMAT(create_time,"%%Y/%%m")'}).values('y_m_date').annotate(c=Count('title')).values_list("y_m_date","c")
    # print(date_list)

    return render(request,'site.html',locals())


def artical(request,username,artical_id):
    user = Userinfo.objects.filter(username=username).all().first()
    blog = user.blog
    artical= Artical.objects.filter(id=artical_id).first()
    comment_list = Comment.objects.filter(artical_id=artical_id)
    print(comment_list)
    return render(request,'artical.html',locals())


from django.db.models import F
import json
from django.http import JsonResponse
from django.db import transaction


def digg(request):
    print(request.POST)
    is_up = json.loads(request.POST.get('is_up'))
    artical_id = request.POST.get('artical_id')
    user_id = request.user.id

    response = {"state":True,"msg":None}

    obj = Aritalupdown.objects.filter(user_id=user_id,artical_id=artical_id).first()
    if obj:
        response['state']=False
        response['handle'] = obj.is_up
    else:
        with transaction.atomic():
            new_obj = Aritalupdown.objects.create(user_id=user_id,artical_id=artical_id,is_up=is_up)
            if is_up:
                Artical.objects.filter(id=artical_id).update(up_count=F('up_count')+1)
            else:
                Artical.objects.filter(id=artical_id).update(down_count=F('down_count')+1)


    return JsonResponse(response)

def comment(request):
    artical_id=request.POST.get('artical_id')
    print(artical_id)
    content=request.POST.get('content')
    print(content)
    pid=request.POST.get('pid')
    print(pid)
    user_id = request.user.id
    print(user_id)
    with transaction.atomic():
        comment=Comment.objects.create(user_id=user_id,content=content,artical_id=artical_id, parent_comment_id=pid)
        Artical.objects.filter(id=artical_id).update(comment_count=F('comment_count')+1)
    response={"state":True}
    response["timmer"]=comment.create_time
    response["content"]=comment.content
    response["user"]=request.user.username

    return JsonResponse(response)


def backend(request):
    user = request.user
    artical_list =Artical.objects.filter(user=user)
    return render(request,'backend/backend.html',locals())


def add_article(request):
    if request.method=="POST":

        title=request.POST.get("title")
        print(title)
        content=request.POST.get("content")
        print(content)
        user=request.user
        print(user)
        category_id=request.POST.get("category")
        print(category_id)
        tags_pk_list=request.POST.getlist("tags")
        print(tags_pk_list)


        soup = BeautifulSoup(content, "html.parser")
        # 文章过滤：
        for tag in soup.find_all():
            # print(tag.name)
            if tag.name in ["script",]:
                tag.decompose()

        desc=soup.text[0:150]

        article_obj=Artical.objects.create(title=title,content=str(soup),user=user,category_id=category_id,abstract =desc)

        for tag_pk in tags_pk_list:
            Artical2Tag.objects.create(article_id=article_obj.pk,tag_id=tag_pk)
        reverse('backend')
        return redirect('backend')


    else:

        blog=request.user.blog
        category_list=Category.objects.filter(blog=blog)
        tags=Tag.objects.filter(blog=blog)
        return render(request,"backend/add_artical.html",locals())

import os
from BBS1 import settings
def upload(request):
    obj=request.FILES.get("upload_img")
    name=obj.name

    path=os.path.join(settings.BASE_DIR,"static","upload",name)
    with open(path,"wb") as f:
        for line in obj:
            f.write(line)

    res={
        "error":0,
        "url":"/static/upload/"+name
    }

    return HttpResponse(json.dumps(res))