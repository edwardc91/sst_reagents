# -*- coding: utf-8 -*-
from django.contrib import admin
from models import UserInfo

from django.db import DatabaseError


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user_auth','local']
