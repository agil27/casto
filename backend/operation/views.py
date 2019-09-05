from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Operation
import uuid
import pytz
import datetime
import time
import os
import sys
import urllib.request
import urllib.error

sys.path.append('../')
from user.models import User

# Create your views here.


UPLOAD_PATH = 'operation/static/operation/images'
BRIEF_PATH = 'operation/images'

if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)


@login_required
def upload(request):
    file_local = request.FILES.get('image', None)
    file_web = request.POST.get('url', None)
    if file_web:
        file_web = file_web.strip()
    if file_local is None and file_web is None:
        return HttpResponse(status=400)
    image_name = str(uuid.uuid1())
    path = os.path.join(UPLOAD_PATH, image_name)
    if file_local is not None:
        raw_name = file_local.name
        _, suffix = os.path.splitext(raw_name)
        if not suffix in ['.jpg', '.JPEG', '.jpeg']:
            return JsonResponse({'error': 'wrong jpeg format'})
        path += suffix
        with open(path, 'wb') as file:
            for chuck in file_local.chunks():
                file.write(chuck)
    else:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
        }
        print(file_web)
        req = urllib.request.Request(file_web, headers=header)
        try:
            with urllib.request.urlopen(req) as f:
                response_data = f.read()
        except urllib.error.HTTPError:
            return JsonResponse({'error': 'fail to download'})
        raw_name = file_web.split('/')[-1][-128:]
        path += '.jpg'
        with open(path, 'wb') as file:
            file.write(response_data)
    operation = Operation.objects.create(
        raw_image=path,
        raw_image_name=raw_name,
        user_id=request.user.id
    )
    operation.save()
    return JsonResponse({'id': operation.id, 'addr': os.path.join(BRIEF_PATH, image_name) + '.jpg'})


@login_required
def net(request, net_id):
    user_id = request.user.id
    operation_id = request.POST.get('id', None)
    if operation_id is None:
        return JsonResponse({'error': 'not exists'})
    operation = Operation.objects.get(id=operation_id)
    if operation.user_id != user_id:
        return JsonResponse({'error': 'not exists'})
    if net_id == 0:
        # TODO processed_path = net(raw_path)
        processed_path = operation.raw_image  # TODO delete later
        operation.net = '0'
    else:
        # TODO processed_path = net(raw_path)
        processed_path = operation.raw_image  # TODO delete later
        operation.net = '1'
    operation.processed_image = processed_path
    operation.save()
    return JsonResponse({'data': read_image_from(processed_path)})


@login_required
def delete(request):
    user_id = request.user.id

    def delete_operation(operation_id):
        try:
            operation = Operation.objects.get(id=operation_id)
        except KeyError:
            return False
        if operation.user_id != user_id:
            return False
        else:
            operation.delete()
            return True

    ids = request.POST.get('ids', [])
    res = [{'id': id_, 'state': delete_operation(id_)} for id_ in ids]
    return JsonResponse({'list': res})


@login_required
def query(request):
    start = request.POST.get('start', 0)
    end = request.POST.get('end', 9999999999)
    start_time = datetime.datetime.fromtimestamp(start, tz=pytz.timezone('UTC'))
    end_time = datetime.datetime.fromtimestamp(end, tz=pytz.timezone('UTC'))
    user_id = request.user.id
    query_set = Operation.objects.filter(user_id=user_id) \
        .filter(upload_time__gt=start_time) \
        .filter(upload_time__lt=end_time) \
        .filter(processed_image__in=['0', '1']) \
        .order_by('-upload_time')
    return render(request, 'user/dashboard.html', {
        'list': [get_operation_info(op) for op in query_set]
    })
    # return JsonResponse({'list': [get_operation_info(op) for op in query_set]})


@login_required
def get(request, operation_id):
    user_id = request.user.id
    try:
        operation = Operation.objects.get(id=operation_id)
    except KeyError:
        return JsonResponse({'error': 'not exists'})
    if operation.user_id != user_id:
        return JsonResponse({'error': 'not exists'})
    return JsonResponse(get_operation_info(operation))


@login_required
def query_admin(request):
    user = request.user
    if not user.admin:
        return JsonResponse({'error': 'permission denied'})
    start = request.POST.get('start', 0)
    end = request.POST.get('end', 9999999999)
    start_time = datetime.datetime.fromtimestamp(start, tz=pytz.timezone('UTC'))
    end_time = datetime.datetime.fromtimestamp(end, tz=pytz.timezone('UTC'))
    username = request.POST.get('username', [])
    if not username:
        user_ids = [u.id for u in User.objects.all()]
    else:
        user_ids = [User.objects.get(username=name).id for name in username]
    query_set = Operation.objects.filter(user_id__in=user_ids) \
        .filter(upload_time__gt=start_time) \
        .filter(upload_time__lt=end_time) \
        .filter(net__in=['0', '1']) \
        .order_by('-upload_time')
    return JsonResponse({'list': [get_operation_info_admin(op) for op in query_set]})


@login_required
def delete_admin(request):
    user = request.user
    if not user.admin:
        return JsonResponse({'error': 'permission denied'})

    def delete_operation(operation_id):
        try:
            operation = Operation.objects.get(id=operation_id)
        except KeyError:
            return False
        operation.delete()
        return True

    ids = request.POST.get('ids', [])
    res = [{'id': id_, 'state': delete_operation(id_)} for id_ in ids]
    return JsonResponse({'list': res})


def get_operation_info(operation):
    return {
        'id': operation.id,
        'time': time.mktime(operation.upload_time.timetuple()),
        'raw': operation.raw_image,
        'name': operation.raw_image_name,
        'processed': operation.processed_image,
        'type': operation.net
    }


def read_image_from(path):
    try:
        with open(path, 'rb') as f:
            data = f.read()
    except IOError:
        return None
    return data


def get_operation_info_admin(operation):
    info = get_operation_info(operation)
    try:
        username = User.objects.get(id=operation.user_id).username
    except KeyError:
        username = 'unknown'
    info['username'] = username
    return info
