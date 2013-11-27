# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from zotero.models import ItemType, Field


def itemtype_fields_view(request):
    itemtype_id = request.GET.get("itemtype")
    obj_item_type = ItemType.objects.get(id=itemtype_id)
    fields = obj_item_type.get_fields()
    field_ids = [f.id for f in fields]
    json_fields = json.dumps(field_ids)
    return HttpResponse(json_fields, content_type='text/javascript')


#test
from django.shortcuts import render
from zotero.forms import DocumentForm, get_tag_formset
from zotero.models import Document

def index(request):
    documents = Document.objects.all()
    context = {'documents': documents}
    return render(request, 'zotero/document/index.html', context)

def detail(request, doc_id):
    obj = Document.objects.get(pk=doc_id)
    
    form = DocumentForm(instance=obj)
    formset = get_tag_formset(obj, labels={'item_type': 'Document type'})
    if request.POST:
        form = DocumentForm(instance=obj, data=request.POST)
        formset = get_tag_formset(obj, data=request.POST)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
    
    return render(request, 'zotero/document/detail.html', {'form2': form, 'formset': formset})
