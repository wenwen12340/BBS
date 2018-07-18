from django import template
register = template.Library()
from blog.models import Category,Userinfo,Tag,Artical
from django.db.models import Count
@register.inclusion_tag('left_region.html')
def get_query_data(username):
    user = Userinfo.objects.filter(username=username).first()
    blog = user.blog
    category_list = Category.objects.filter(blog=blog, artical__user__username=user.username).annotate(
        c=Count('artical__title')).values_list('title', 'c')
    # print(category_list)

    tag_list = Tag.objects.filter(blog=blog, artical__user__username=user.username).annotate(
        c=Count('artical__title')).values_list('title', 'c')
    # print(tag_list)

    date_list = Artical.objects.filter(user=user).extra(
        select={'y_m_date': 'DATE_FORMAT(create_time,"%%Y/%%m")'}).values('y_m_date').annotate(
        c=Count('title')).values_list("y_m_date", "c")
    print(date_list)
    return {'blog':blog,"username":username,'category_list':category_list,'tag_list':tag_list,'date_list':date_list}

