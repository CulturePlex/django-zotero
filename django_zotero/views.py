# -*- coding: utf-8 -*-
import json
from django.conf import settings
from django.http import HttpResponse
from django_zotero.models import ItemType, Field
from os.path import abspath, dirname, join, pardir


def itemtype_fields_view(request):
    itemtype_id = request.GET.get("itemtype")
    obj_item_type = ItemType.objects.get(id=itemtype_id)
    fields = obj_item_type.get_fields()
    field_ids = [f.id for f in fields]
    json_fields = json.dumps(field_ids)
    return HttpResponse(json_fields, content_type='text/javascript')


def valid_zotero_itemtypes_fields(request):
    path = abspath(
        join(dirname(__file__),
        'media/valid_zotero_itemtypes_and_fields.txt'))
    itemtypes_fields = {}
    for line in open(path):
        if line and not line.startswith('#'):
            line = line.strip()
            itemtype = line.split(':')[0]
            fields = line.split(':')[1]
            fields = fields.split(',')
            itemtype_id = ItemType.objects.get(type_name=itemtype).id
            field_ids = [Field.objects.get(field_name=field).id for field in fields]
            itemtypes_fields[itemtype_id] = field_ids
    json_itemtypes_fields = json.dumps(itemtypes_fields)
    return HttpResponse(json_itemtypes_fields, content_type='text/javascript')


#test
from django.shortcuts import render
from django_zotero.forms import DocumentForm, get_tag_formset
from django_zotero.models import Document

def index(request):
    documents = Document.objects.all()
    context = {'documents': documents}
    return render(request, 'zotero/document/index.html', context)

def detail(request, doc_id):
    obj = Document.objects.get(pk=doc_id)
    
    form = DocumentForm(instance=obj)
    formset = get_tag_formset(obj, show_labels=False, labels={'item_type': 'Document type'})
    if request.POST:
        form = DocumentForm(instance=obj, data=request.POST)
        formset = get_tag_formset(obj, data=request.POST, labels={'item_type': 'Document type'})
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
    
    return render(request, 'zotero/document/detail.html', {'form2': form, 'formset': formset})
