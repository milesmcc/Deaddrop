# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from .models import Drop, Client, SecurityQuestion, Login, Download
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import datetime
import pytz

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def login(request, client):
    request.session['logged_in'] = True
    request.session['code'] = client.code
    request.session['id'] = str(client.id)
    request.session.set_expiry(client.session_time)
    Login(client=client, successful=True, ip=get_client_ip(request)).save()

def logout(request):
    request.session.flush()

def IndexView(request):
    if 'logged_in' in request.session and request.session['logged_in']:
        # they are logged in and good to go
        if 'id' not in request.session:
            return CodeView(request, error="Please re-enter your secure access code.")
        id = request.session['id']
        client = Client.objects.get(id=id)
        return DropsView(request, client)
    elif 'logged_in' in request.session and request.session['logged_in'] == False and 'code' in request.session:
        # they aren't logged in, but have submitted a code
        code = request.session['code']
        client = Client.objects.get(code=code)
        securityquestions = SecurityQuestion.objects.filter(client=client)
        if len(securityquestions) > 0:
            return SecurityQuestionView(request, client)
        else:
            login(request, client)
            return redirect("securecore:index")
    else:
        # they aren't logged in.
        if request.session is not None:
            request.session.flush()
        return CodeView(request)

def CodeView(request, special_message="Enter your secure access code.", error=None, success=None):
    request.session.flush() # for hightened security
    context = {
        "greeting": special_message,
        "logged_in": False,
        "client": None,
        "error": error,
        "success": success,
    }
    return render(request, "securecore/code.html", context)

def AuthCodeMethod(request):
    if request.POST:
        code = request.POST['code']
        try:
            client = Client.objects.get(code=code)
            request.session['logged_in'] = False
            request.session['code'] = code
            request.session['id'] = str(client.id)
            request.session.set_expiry(600) # 10 minutes
            return redirect("securecore:index")
        except ObjectDoesNotExist:
            request.session.flush()
            return CodeView(request, error="Invalid secure access code.")
    return redirect("securecore:index")

def AuthSecurityQuestionMethod(request):
    if request.POST and ('logged_in' not in request.session or request.session['logged_in'] is False) and 'id' in request.session:
        client = Client.objects.get(id=request.session['id'])
        security_questions = SecurityQuestion.objects.filter(client=client)
        incorrect = []
        ok = True
        for question in security_questions:
            answer = request.POST[str(question.id)]
            if not question.verify(answer):
                ok = False
                incorrect.append(question.id)
        if not ok:
            Login(client=client, successful=False, ip=get_client_ip(request)).save() # incorrect login attempt!
            return SecurityQuestionView(request, client, error=("Incorrect response(s)."), incorrect=incorrect)
        if client:
            login(request, client)
            return redirect("securecore:index")
        else:
            request.session.flush()
    return CodeView(request, error="Please re-enter your secure access code.")

def LogoutMethod(request):
    logout(request)
    return CodeView(request, success="You have been successfully logged out.")

def SecurityQuestionView(request, client, success=None, error=None, special_message="Please verify your identity.", incorrect=[]):
    context = {
        "client": client,
        "greeting": special_message,
        "securityquestions": SecurityQuestion.objects.filter(client=client),
        "request": request,
        "logged_in": False,
        "success": success,
        "error": error,
        "incorrect": incorrect
    }
    return render(request, "securecore/securityquestions.html", context)

def DropsView(request, client):
    context = {
        "drops": [drop for drop in Drop.objects.filter(client=client).order_by("-modified_date").filter() if not drop.is_expired()],
        "client": client,
        "logged_in": True
    }
    return render(request, "securecore/drops.html", context)

def DropView(request, drop_uuid):
    if request.session is None or 'logged_in' not in request.session or request.session['logged_in'] == False or 'id' not in request.session or request.session['id'] is None:
        return redirect("securecore:code")
    client = Client.objects.get(id=request.session['id'])
    context = {
        "drop": get_object_or_404(Drop, id=drop_uuid),
        "client": client,
        "request": request,
        "logged_in": True
    }
    if context['drop'].client != client:
        raise Http404() # needs to be identitcal response to get_object_or_404 to prevent 'association' attacks
    if context['drop'].is_expired():
        raise Http404() # ...as though it never existed!
    context['client'] = context['drop'].client
    return render(request, "securecore/drop.html", context)

def DownloadDropView(request, drop_uuid):
    if 'logged_in' in request.session and request.session['logged_in']:
        client = Client.objects.get(id=request.session['id'])
        drop = Drop.objects.get(id=drop_uuid)
        if drop.client == client and not drop.is_expired():
            Download(client=client, successful=True, ip=get_client_ip(request), drop=drop).save()
            drop.downloads += 1
            drop.save()
            filename = drop.file.name.split('/')[-1]
            response = HttpResponse(drop.file, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response
    return redirect("securecore:index")
