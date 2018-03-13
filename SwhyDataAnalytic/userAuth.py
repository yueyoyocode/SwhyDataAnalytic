'''
用户登录，登出处理，应用django自带的权限处理机制
数据库有auth_user表存储的用户数据模型
这里只需要应用逻辑就行了

可以按照角色赋权，也可以按照用户赋权
'''

from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
import logging


#创建用户
def createUser(request):
    userName = request.POST.get('userName')
    userEmail = request.POST.get('userEmail')
    userPassword = request.POST.get('userPassword')
    user = User.objects.create_user(userName, userEmail, userPassword)
    user.save()

#修改密码
def changePwd(request):
    userName = request.POST.get('userName')
    userOldPassword = request.POST.get('userOldPassword')
    userNewPassword = request.POST.get('userNewPassword')
    user = authenticate(username=userName, password=userOldPassword)
    if user is not None:
        user.set_password(userNewPassword)
        user.save()

#登录
def userLogin(request):
    userName = request.POST.get('userName')
    userPassword = request.POST.get('userPassword')
    user = authenticate(username=userName, password=userPassword)
    if user is not None:
        login(request, user)
    else:
        logging.error("用户名或者密码错误！")
#退出
def userLogout(request):
    logout(request)
    #重定向地址
    return redirect('/login/?next=%s' % request.path)

#保持登录状态
def userAll(request):
    if request.user.is_authenticated:
        user_name=request.user
    else:
        user_name=''
    return render(request, 'news.html', {
        'user_name': user_name,
    })

#添加角色
def addGroup(request):
    groupName = request.POST.get('groupName')
    group = Group.objects.create(name=groupName)
    group.save()

#修改角色权限
def addPermission2Group(request):
    groupName = request.POST.get('groupName')
    groupPermission = request.POST.get('groupPermission')
    method = request.POST.get('method')
    group = Group.objects.get(name=groupName)
    #操作判断
    if(method == 'add'):
        group.permissions.add(groupPermission)
    elif(method == 'delete'):
        group.permissions.delete(groupPermission)
    elif(method == 'clear'):
        group.permissions.clear()

#修改用户权限
def addPermission2User(request):
    userName = request.POST.get('userName')
    userPassword = request.POST.get('userPassword')
    userPermission = request.POST.get('userPermission')
    method = request.POST.get('method')

    user = authenticate(username=userName, password=userPassword)
    if user is not None:
        # 操作判断
        if (method == 'add'):
            user.permissions.add(userPermission)
        elif (method == 'delete'):
            user.permissions.delete(userPermission)
        elif (method == 'clear'):
            user.permissions.clear()
    else:
        logging.error("用户名或者密码错误！")
