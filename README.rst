django-zotero
=============
django-zotero_ is a django_ app that provides a generic formset to tag any django_ object with Zotero_ metadata. Tagged object are easily exportable to Zotero_ in one click.


Installation
------------
First of all, it is needed to have pip_ installed on your system. It is strongly recommended to install virtualenv_ and virtualenvwrapper_ to take the most advantage of pip_.

To install pip_, go to http://www.pip-installer.org/en/latest/installing.html

To install virtualenv_, go to https://pypi.python.org/pypi/virtualenv

To install virtualenvwrapper_, go to http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation

Now install django-zotero_::

    $ pip install django-zotero


Usage
-----
To use django-zotero_, follow the next steps:

1) Django settings: add the app name to INSTALLED_APPS in settings.py::

    INSTALLED_APPS = (
        #...,
        'zotero',
    )

2) Administration side: add the following code to admin.py:

   a) Import the class TagInlineAdmin [#]_::

       from zotero.admin import TagInlineAdmin

   b) For each model you wish to tag, add to its admin class::

       inlines = (
           #...,
           TagInlineAdmin,
       )

3) User side: add the following code:

   a) In views.py:

      i) Import the function get_tag_formset [#]_::

          from zotero.forms import get_tag_formset

      ii) In the view that manages the tagged object, instanciate the formset and save it::

           tag_formset = get_tag_formset(
               obj=form.instance,
               data=request.POST,
               show_labels=False,
               labels={
                   'item_type': 'Document type',
                   #...,
               }
           )
           #...
           tag_formset.save()

   b) In the template that manages the object:

      i) Import the template tag zotero_inline_tags [#]_::

          {% load zotero_inline_tags from zotero_inline_extras %}

      ii) Render the formset::

          {% zotero_inline_tags formset %}

   c) In the template that renders the object:

      i) Import the template tag zotero_tags [#]_::

          {% load zotero_tags from zotero_tags_extras %}

      ii) Render Zotero_ metadata::

           {% zotero_tags
               object=document
               vocabulary="dc"
               output_method="meta" %}

.. [#] TagInlineAdmin is an inline class ready to be added as inline of other admin class.
.. [#] get_tag_formset is a function that gets the formset with Zotero tags for an object. It is based on a generic formset factory and takes four arguments:

 1) `obj`: object to tag

 2) `data`: data to instanciate the content of the formset

 3) `show_labels`: if true, show the labels as headers on the top of the formset; if false, show the labels as placeholders

 4) `labels`: set alternative labels - default labels are 'item_type', 'field' and 'value'

.. [#] zotero_inline_tags is a template tag that renders a formset. It takes one argument: the formset it renders.
.. [#] zotero_tags is a template tag that renders the HTML code of Zotero_ metadata. It takes three arguments:

 1) `object`: tagged object

 2) `vocabulary`: the vocabulary to code the metadata - currently it works with Dublin Core ("dc")

 3) `output_method`: the method to code the metadata - currently it works HTML <meta> tags ("meta")

.. _django-zotero: https://pypi.python.org/pypi/django-zotero/0.1
.. _django: https://www.djangoproject.com/
.. _Zotero: http://www.zotero.org/
.. _pip: https://pypi.python.org/pypi/pip
.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/

