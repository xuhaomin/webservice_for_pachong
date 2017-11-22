import time
import json

from django.http import HttpResponse

from proxy_service.models import VPS


def get_proxy(request):
    try:
        proxy_ip = VPS.objects.order_by('-scvp_create_time')[0:1].get()
    except Exception as e:
        proxy_ip = ''
    if proxy_ip:
        content = proxy_ip.ip()
        status = 200
    else:
        content = json.dumps(
            {"status": "failed", "msg": "参数错误或无结果"}, ensure_ascii=False)
        status = 201
    return HttpResponse(content=content, status=status)


def add_proxy(request):
    if request.method == "POST":
        scvp_vps_name = request.POST.get('vps_name', '')
    elif request.method == "GET":
        scvp_vps_name = request.GET.get('vps_name', '')
    remote_ip = request.META.get('REMOTE_ADDR', '')
    vps_proxy = request.META.get('HTTP_X-Real-Ip', remote_ip)

    if scvp_vps_name and vps_proxy:
        proxy_ip = vps_proxy + ':19988'
        data = VPS(scvp_vps_name=scvp_vps_name, scvp_vps_proxy=proxy_ip,
                   scvp_create_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        data.save()
        content = json.dumps(
            {"status": "ok", "msg": "插入成功"}, ensure_ascii=False)
        status = 200
    else:
        content = json.dumps(
            {"status": "failed", "msg": "非法请求"}, ensure_ascii=False)
        status = 403
    return HttpResponse(content=content, status=status)
