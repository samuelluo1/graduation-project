import token

from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.utils import json
from django.contrib.auth.models import User

class LoginView(View):
    def get(self, request):
        return token.token(request)

    def post(self, request):
        """登入校驗"""
        # 接收數據
        username = json.loads(request.body.decode('utf-8'))["username"]
        password = json.loads(request.body.decode('utf-8'))["password"]
        # 校驗數據
        info = {}
        if not all([username, password]):
            # 數據不完整
            info['msg'] = '信息不完整'
            return HttpResponse(json.dumps(info))
        # 登入校驗
        user = authenticate(username=username, password=password)
        if user is not None:  # 用戶名密码正確
            # 記錄用户的登入狀態
            # login(request, user)
            request.session['username'] = user.username
            request.session['is_login'] = True

            info['msg'] = '登入成功'
            info['result'] = '登入成功'
            res = HttpResponse()
            res.content = json.dumps(info)
            res.set_cookie('username', username)
            return res

        else:
            # 用戶名或密碼錯誤
            info['msg'] = '用戶名或密碼錯誤'
            info['result'] = '登入錯誤'
            return HttpResponse(json.dumps(info))
