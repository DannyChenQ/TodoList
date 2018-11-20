# coding:utf-8
"""
created by 2016-12-30
@auther:cdq
"""
from django.shortcuts import render, render_to_response, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
import json
from common import DBAction, DBActionMYSQL
from log_echo.echo_log import Echo_Log
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q

log = Echo_Log(level=20)
db = DBAction()


# Create your views here.

def mytodolist(request):
    MYSQL_db = DBActionMYSQL()
    if not request.user.is_authenticated():
        return log_in(request)
    result = db.query(request.user.id)
    page_num = request.GET.get("page", 1)
    for data in result:
        data.add_time = str(data.add_time)

    paginator = Paginator(result, 5)
    try:
        result = paginator.page(page_num)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    log.info("query todolist.......")
    news_result = MYSQL_db.query()
    return render_to_response('index.html', {"result": result, "username": request.user.username, "news": news_result},
                              context_instance=RequestContext(request))


def add(request):
    if request.method == "POST":
        response_data = {"code": 1, "msg": "error"}
        content = request.POST.get("content", "")
        level = request.POST.get("level", "")
        is_complete = request.POST.get("is_complete", "")
        time_minute = request.POST.get("time_minute", "")
        time_day = request.POST.get("time_day", "")
        time_hours = request.POST.get("time_hours", "")
        if not time_hours:
            time_hours = "0"
        if not time_day:
            time_day = "0"
        if not time_minute:
            time_minute = "0"
        if content:
            response_data['code'] = 0
            data = {
                "user_id": request.user.id,
                "content": content,
                "level": level,
                "is_complete": is_complete,
                "time_day": time_day,
                "time_hours": time_hours,
                "time_minute": time_minute,
            }
            db.create(**data)
        if response_data['code'] == 1:
            log.error("add todolist  content is '' .....")
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        log.error("add todolist method is GET...........")
        return HttpResponse("error")


def complete(request):
    id = request.POST.get("id", "")
    if id:
        db.update(id)
    log.info("complete todolist >>%s" % id)
    return HttpResponse(json.dumps({"code": 0, "msg": 'success'}), content_type="application/json")


def delete(request):
    id = request.POST.get("id", "")
    if id:
        db.del_list(id)
        log.info("delete todolist >> %s" % id)
    return HttpResponse(json.dumps({"code": 0, "msg": 'success'}), content_type="application/json")


def update(request):
    id = request.POST.get("id", "")
    content = request.POST.get("content", "")
    print id, content,
    if id and content:
        db.updata_content(id, content)
    log.info("update content >>%s" % content)
    return HttpResponse(json.dumps({"code": 0, "msg": 'success'}), content_type="application/json")


def search(request):
    query = request.GET.get("q", "")
    qset = ()
    result = []
    if query:
        qset = (
            Q(content__icontains=query) |
            Q(add_time__icontains=query) |
            Q(time_day__icontains=query) |
            Q(time_hours__icontains=query)
        )
        result = db.search_all(request.user.id, q_set=qset)
    else:
        result = db.query(request.user.id)
    page_num = request.GET.get("page", 1)
    for data in result:
        data.add_time = str(data.add_time)
    paginator = Paginator(result, 5)
    try:
        result = paginator.page(page_num)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    log.info("query todolist.......")
    return render_to_response('index.html', {"result": result, "username": request.user.username},
                              context_instance=RequestContext(request))


def log_in(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        log.info("login >> %s " % username)
        request.session.set_expiry(6000)
        return HttpResponseRedirect("/todolist/")
    return render(request, "login.html")


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/todolist/login")


def registered(request):
    username = request.POST.get("username", "")
    passwd = request.POST.get("password", "")
    passwd1 = request.POST.get("password1", "")
    if request.method == "POST":
        if username and passwd and passwd1:
            if passwd == passwd1:
                user = User.objects.create_user(username=username, email="54457@qq.com", password=passwd)
                log.info("registed >>%s" % user)
                return HttpResponseRedirect("/todolist/login")
            else:
                return HttpResponseRedirect("/todolist/reg")
        else:
            return HttpResponseRedirect("/todolist/reg")
    else:
        return render(request, "reg.html")


def check_time():
    print "this is tasks"