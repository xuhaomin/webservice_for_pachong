from django.http import HttpResponse
import json
import time

from crawler.models import Machine, Spider, Task


def add_machine(request):
    if request.method == "POST":
        machine_name = request.POST.get('machine_name', '')
        machine_ip = request.POST.get('machine_ip', '')
    elif request.method == "GET":
        machine_name = request.GET.get('machine_name', '')
        machine_ip = request.GET.get('machine_ip', '')
    if machine_name and machine_ip:
        data = Machine(machine_name=machine_name, machine_ip=machine_ip)
        data.save()
        content = json.dumps(
            {"status": "ok", "msg": "插入成功"}, ensure_ascii=False)
        status = 200
    else:
        content = json.dumps(
            {"status": "failed", "msg": "非法请求"}, ensure_ascii=False)
        status = 403
    return HttpResponse(content=content, status=status)


def get_machine(request):
    '''
    return list of machines
    '''
    resp_data = []
    machines = Machine.objects.all()
    for machine in machines:
        resp_data.append(machines.machine_name)
    content = json.dumps(resp_data)
    status = 200
    return HttpResponse(content=content, status=status)


def add_spider(request):
    if request.method == "POST":
        spider_name = request.POST.get('spider_name', '')
        site = request.POST.get('site', '')
    elif request.method == "GET":
        spider_name = request.GET.get('spider_name', '')
        site = request.GET.get('site', '')
    if spider_name and site:
        data = Spider(spider_name=spider_name, site=site)
        data.save()
        content = json.dumps(
            {"status": "ok", "msg": "插入成功"}, ensure_ascii=False)
        status = 200
    else:
        content = json.dumps(
            {"status": "failed", "msg": "非法请求"}, ensure_ascii=False)
        status = 403
    return HttpResponse(content=content, status=status)


def task_begin(request):
    if request.method == "POST":
        spider_name = request.POST.get('spider_name', '')
        machine_name = request.POST.get('machine_name', '')

    elif request.method == "GET":
        spider_name = request.GET.get('spider_name', '')
        machine_name = request.GET.get('machine_name', '')

    try:
        spider = Spider.object.get(spider_name__exact=spider_name)
        machine = Machine.object.get(machine_name__exact=machine_name)
    except Exception as e:
        content = json.dumps(
            {"status": "failed", "msg": "找不到spider/machine"},
            ensure_ascii=False
        )
        status = 403
        return HttpResponse(content=content, status=status)

    is_running = True
    begin_time = time.strftime("%Y-%m-%d %H:%M:%S")

    if spider and machine:
        data = Task(spider=spider, machine=machine,
                    is_running=is_running, begin_time=begin_time)
        data.save()
        content = json.dumps(
            {"status": "ok", "msg": "任务开始"}, ensure_ascii=False)
        status = 200
    else:
        content = json.dumps(
            {"status": "failed", "msg": "参数错误"}, ensure_ascii=False)
        status = 403
    return HttpResponse(content=content, status=status)


def task_done(request):
    if request.method == "POST":
        spider_name = request.POST.get('spider_name', '')
        machine_name = request.POST.get('machine_name', '')

    elif request.method == "GET":
        spider_name = request.GET.get('spider_name', '')
        machine_name = request.GET.get('machine_name', '')

    is_running = False
    end_time = time.strftime("%Y-%m-%d %H:%M:%S")

    if spider_name and machine_name:
        datas = Task.object.filter(
            spider__spider_name__exact=spider_name).filter(
            machine__machine_name__exact=machine_name)
        if len(datas) == 0:
            content = json.dumps(
                {"status": "failed", "msg": "找不到spider/machine"},
                ensure_ascii=False
            )
            status = 403
            return HttpResponse(content=content, status=status)
        data = datas[0]
        data.is_running = is_running
        data.end_time = end_time
        data.save()
        content = json.dumps(
            {"status": "ok", "msg": "任务结束"}, ensure_ascii=False)
        status = 200
    else:
        content = json.dumps(
            {"status": "failed", "msg": "参数错误"}, ensure_ascii=False)
        status = 403
    return HttpResponse(content=content, status=status)


def format_dict(data):
    if len(data) == 1:
        return {'name': data.pop('time'), 'value': [0, '', '']}
    elif len(data) > 1:
        time = data.pop('time')
        max_key = max(data, key=data.get)
        max_value = data.pop(max_key)
        if data:
            rest = json.dumps(data)
        else:
            rest = ''
        return {'name': time, 'value': [max_value, max_key, rest]}
