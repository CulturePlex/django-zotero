# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
import django
from django.contrib.contenttypes import generic
from django.forms.models import inlineformset_factory

from zotero.forms import GenericTagInlineForm, GenericTagInlineFormset, DocumentForm, get_tag_formset
from zotero.models import Document, Tag

def index(request):
    documents = Document.objects.all()
    context = {'documents': documents}
    return render(request, 'zotero/document/index.html', context)

def detail(request, doc_id):
    obj = Document.objects.get(pk=doc_id)
    
    form = DocumentForm(instance=obj)
    formset = get_tag_formset(obj)
    if request.POST:
        form = DocumentForm(instance=obj, data=request.POST)
        formset = get_tag_formset(obj, data=request.POST)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
    
    return render(request, 'zotero/document/detail.html', {'form': form, 'formset': formset})
