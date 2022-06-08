import datetime
import string
from urllib import response
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
import secrets
import numpy as np
from functools import partial
from django.db import IntegrityError, transaction
from authapp.models import User
from shortenurl import common
from shortenurl.models import Shortener
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


def produce_amount_keys(amount_of_keys, _randint=np.random.randint):
    timestamp1 = datetime.datetime.now()
    keys = set()
    pickchar = partial(secrets.choice, string.ascii_uppercase + string.digits)
    while len(keys) < amount_of_keys:
        keys |= {''.join([pickchar() for _ in range(_randint(12, 20))]) for _ in range(amount_of_keys - len(keys))}
    timestamp2 = datetime.datetime.now()
    seconds_in_day = 24 * 60 * 60
    diff = ( timestamp2 - timestamp1)
    diff = divmod(diff.days * seconds_in_day + diff.seconds, 60)
    return keys, diff


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def create_shortener_link(request):
    try:
        
        user_obj = User.objects.get(id=request.user.id)
        context = {
        'status': status.HTTP_200_OK,
        'result': 'no result',
        }
        if request.method == 'GET':
            url = request.GET["url"]
            prefer_str = request.GET["prefer_str"]
            auto = request.GET["auto"]
        elif request.method == 'POST':
            url = request.POST.get("url", None)
            prefer_str = request.POST.get("prefer_str", None)
            auto = request.POST.get("", False)
        else:
           
            context['status'] = status.HTTP_400_BAD_REQUEST 
            context['result'] = '{}'.format(common.GENERAL_ERROR)
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
        auto = False if 'False' in str(auto) else True
        print(auto)
        if (not common.valid_url(url)):
            context['status'] = status.HTTP_400_BAD_REQUEST 
            context['result'] = '{}'.format(common.TYPE_ERROR)
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
        if not auto and not common.valid_slug(prefer_str):
            context['status'] = status.HTTP_400_BAD_REQUEST 
            context['result'] = '{}'.format(common.TYPE_SLUG_ERROR)
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            if auto:
                new_key, d_time = produce_amount_keys(1128)
                obj_shortener = Shortener.objects.filter(shortener__in=list(new_key))
                by_key = obj_shortener.distinct().values_list('shortener', flat=True)
                open_links = set(new_key) - set(by_key)
                if len(open_links)>=1:
                    key_to = open_links[0]
                    new_obj = Shortener.objects.create(url=url, shortener=key_to, user=user_obj )
                    new_obj.save()
                    pass
                else:
                    context = {
                    'status': status.BAD_REQ_ERROR,
                    'result': 'Try again',
                    }
            else: #auto == False or None Post or Get
                obj_shortener = Shortener.objects.filter(shortener=prefer_str)
                if not obj_shortener.exists():
                    new_obj = Shortener.objects.create(url=url, shortener=prefer_str, user=user_obj)
                    new_obj.save()
                    context = {
                    'status': status.HTTP_200_OK,
                    'result': 'Shortener-url created',
                    }
                else:
                    context = {
                    'status': status.HTTP_201_CREATED,
                    'result': 'Url already taken',
                    }
    except IntegrityError:
        print('1')
        context = {
        'status': status.BAD_REQ_ERROR,
        'result': 'no result',
        }
        pass
    except Exception as exr:
        print(str(exr))
        context = {
        'status': status.HTTP_400_BAD_REQUEST,
        'result': 'no result',
        }
        pass
    return Response(data=context, status=context['status'])


def redirect_view(request, slug):
    try:
        shortener = Shortener.objects.get(shortener=slug)
        return HttpResponseRedirect(shortener.url)
    except Shortener.DoesNotExist:
        msg = ('Link does not exist. ')
    except:
       msg = ('Link is broken. ')
    raise Http404(msg)