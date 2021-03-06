from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from .models import Operation
from .net.Detector import Detector
from .net.GenderSwapper import Swapper
import uuid
import datetime
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

detector = Detector()
swapper = Swapper()


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
        path += '.jpg'
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
        net_ = detector
        try:
            processed_path, crop_path = net_(operation.raw_image)
        except Exception:
            return JsonResponse({'error': 'fail to trans'})
        new_op = Operation.objects.create(
            raw_image=operation.raw_image,
            crop=crop_path,
            emotion=processed_path,
            type='0',
            user_id=user_id
        )
        new_op.save()
        type_ = 'emotion'
    else:
        net_ = swapper
        gender_model_name = request.POST.get('gender')
        try:
            processed_path, crop_path = net_.swapgender(operation.raw_image, gender_model_name)
        except Exception:
            return JsonResponse({'error': 'fail to trans'})
        new_op = Operation.objects.create(
            raw_image=operation.raw_image,
            crop=crop_path,
            gender=processed_path,
            type='1',
            user_id=user_id
        )
        new_op.save()
        type_ = 'gender'
    shrink_processed_path = processed_path[10:]  # rid the first 'operation/
    shrink_crop_path = crop_path[10:]
    return JsonResponse({
        type_: shrink_processed_path,
        'cropped': shrink_crop_path
    })


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
            raw = operation.raw_image
            if len(Operation.objects.filter(raw_image=raw)) == 1:
                try:
                    os.remove(raw)
                except FileNotFoundError:
                    pass
                crop = operation.crop
                try:
                    os.remove(crop)
                except FileNotFoundError:
                    pass
                emotion = operation.emotion
                try:
                    os.remove(emotion)
                except FileNotFoundError:
                    pass
                gender = operation.gender
                try:
                    os.remove(gender)
                except FileNotFoundError:
                    pass
                operation.delete()
                return True
            else:
                operation.delete()
                return False

    ids = request.POST.getlist('ids[]', [])
    res = [{'id': id_, 'state': delete_operation(id_)} for id_ in ids]
    return JsonResponse({'list': res})


@login_required
def query(request):
    user_id = request.user.id
    query_set = Operation.objects \
        .filter(user_id=user_id) \
        .filter(type__in=['0', '1'])
    range_show = request.GET.get('range', 'no')
    rangequery = True if range_show == 'yes' else False
    page = request.GET.get('page', 1)
    start = request.GET.get('start', '01/01/1970 12:00 AM')
    end = request.GET.get('end', '12/31/2100 12:00 PM')
    start_time = datetime.datetime.strptime(start, '%m/%d/%Y %I:%M %p')
    end_time = datetime.datetime.strptime(end, '%m/%d/%Y %I:%M %p')
    query_set = query_set \
        .filter(upload_time__gt=start_time) \
        .filter(upload_time__lt=end_time) \
        .order_by('-upload_time')
    query_set = query_set.order_by('-upload_time')
    list_ = [get_operation_info(op) for op in query_set]
    paginator = Paginator(list_, 10)
    try:
        li_ = paginator.page(page)
    except PageNotAnInteger:
        li_ = paginator.page(1)
    except EmptyPage:
        li_ = paginator.page(paginator.num_pages)
    except InvalidPage:
        li_ = paginator.page(1)
    return render(request, 'user/dashboard.html', {
        'list': li_,
        'username': request.user,
        'npage': list(range(1, paginator.num_pages + 1)),
        'cur': page,
        'prev': max(int(page) - 1, 1),
        'next': min(int(page) + 1, paginator.num_pages),
        'rangequery': rangequery,
        'is_admin': request.user.admin
    })


@login_required
def get(request):
    user_id = request.user.id
    operation_id = request.GET.get('id', -1)
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
    query_set = Operation.objects \
        .filter(type__in=['0', '1'])
    range_show = request.GET.get('range', 'no')
    rangequery = True if range_show == 'yes' else False
    page = request.GET.get('page', 1)
    start = request.GET.get('start', '01/01/1970 12:00 AM')
    end = request.GET.get('end', '12/31/2100 12:00 PM')
    start_time = datetime.datetime.strptime(start, '%m/%d/%Y %I:%M %p')
    end_time = datetime.datetime.strptime(end, '%m/%d/%Y %I:%M %p')
    query_set = query_set \
        .filter(upload_time__gt=start_time) \
        .filter(upload_time__lt=end_time) \
        .order_by('-upload_time')
    query_set = query_set.order_by('-upload_time')
    list_ = [get_operation_info_admin(op) for op in query_set]
    paginator = Paginator(list_, 10)
    try:
        li_ = paginator.page(page)
    except PageNotAnInteger:
        li_ = paginator.page(1)
    except EmptyPage:
        li_ = paginator.page(paginator.num_pages)
    except InvalidPage:
        li_ = paginator.page(1)
    return render(request, 'admin/dashboard.html', {
        'list': li_,
        'npage': list(range(1, paginator.num_pages + 1)),
        'username': user.username,
        'cur': page,
        'prev': max(int(page) - 1, 1),
        'next': min(int(page) + 1, paginator.num_pages),
        'rangequery': rangequery
    })


@login_required
def get_admin(request):
    operation_id = request.GET.get('id', -1)
    try:
        operation = Operation.objects.get(id=operation_id)
    except KeyError:
        return JsonResponse({'error': 'not exists'})
    return JsonResponse(get_operation_info_admin(operation))


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
        raw = operation.raw_image
        if len(Operation.objects.filter(raw_image=raw)) == 1:
            try:
                os.remove(raw)
            except FileNotFoundError:
                pass
            crop = operation.crop
            try:
                os.remove(crop)
            except FileNotFoundError:
                pass
            emotion = operation.emotion
            try:
                os.remove(emotion)
            except FileNotFoundError:
                pass
            gender = operation.gender
            try:
                os.remove(gender)
            except FileNotFoundError:
                pass
            operation.delete()
            return True
        else:
            operation.delete()
            return False

    ids = request.POST.getlist('ids[]', [])
    res = [{'id': id_, 'state': delete_operation(id_)} for id_ in ids]
    return JsonResponse({'list': res})


def get_operation_info(operation):
    e = operation.emotion
    g = operation.gender
    if e and g:
        type_ = '2'
    elif e:
        type_ = '0'
    elif g:
        type_ = '1'
    else:
        type_ = ''
    time = operation.upload_time + datetime.timedelta(hours=8)
    return {
        'id': operation.id,
        'time': time.strftime("%Y-%m-%d %H:%M"),
        'raw': operation.raw_image,
        'name': operation.raw_image_name,
        'crop': operation.crop,
        'emotion': e,
        'gender': g,
        'raw_for_modal': operation.raw_image[10:],
        'emotion_for_modal': e[10:],
        'gender_for_modal': g[10:],
        'type': type_
    }


def get_operation_info_admin(operation):
    info = get_operation_info(operation)
    try:
        username = User.objects.get(id=operation.user_id).username
    except KeyError:
        username = 'unknown'
    info['username'] = username
    return info
