# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 11:37:19 2020

@author: Marcin
"""

from django import forms
from . import models



class PostForm(forms.ModelForm):
    class Meta:
        model = models.Klient
        fields = ('imie','nazwisko','nr_tel')