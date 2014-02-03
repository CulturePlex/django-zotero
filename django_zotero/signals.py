# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django_zotero.models import Tag


@receiver(pre_save, sender=Tag)
def check_save(sender, **kwargs):
    """
    Checks item type uniqueness, field applicability and multiplicity.
    """
    tag = kwargs['instance']
    obj = Tag.get_object(tag)
    previous_tags = Tag.get_tags(obj)
    
    err_uniq = check_item_type_uniqueness(tag, previous_tags)
    err_appl = check_field_applicability(tag)
    err_mult = check_field_multiplicity(tag, previous_tags)
    err_msg = generate_error_message(tag, err_uniq, err_appl, err_mult)
    if err_uniq or err_appl or err_mult:
        raise TypeError(err_msg)


def check_item_type_uniqueness(tag, previous_tags):
    """
    Check the uniqueness of the 'item type' for an object.
    """
    fail = False
    #If the tag is being created...
    if not tag.id:
        #... and the new item type is different from previous item types (for
        #example, different from the first of them), fail
        fail = previous_tags and tag.item_type != previous_tags[0].item_type
    #If the tag is being modifying...
    else:
        #... but there is only one previous tag (the one that is being
        #modifying), do not fail
        fail = previous_tags.count() > 1 and \
               tag.item_type != previous_tags[0].item_type
    return fail


def check_field_applicability(tag):
    """
    Check the applicability of a 'field' for an object.
    """
    #If the new field does not belong to the applicable field list, fail
    return not tag.field in tag.item_type.fields.all()


def check_field_multiplicity(tag, previous_tags):
    """
    Check the multiplicity of a 'field' for an object.
    """
    fail = False
    #If the field is single
    if not tag.field.multiple:
        #If the tag is being created...
        if not tag.id:
            #... and the new field was already included in the previous tags,
            #fail
            fail = previous_tags.filter(field=tag.field)
        #If the tag is being modifying...
        else:
            #... but there is only one previous tag (the one that is being
            #modifying), do not fail
            fail = previous_tags.filter(field=tag.field).count() > 1
    return fail


def generate_error_message(tag, err_uniq, err_appl, err_mult):
    """
    Generate the error message for an object.
    """
    err = []
    if err_uniq:
        err.append('Uniqueness restriction: item type %s' % tag.item_type)
    if err_appl:
        err.append('Applicability restriction: field %s' % tag.field)
    if err_mult:
        err.append('Multiplicity restriction: field %s' % tag.field)
    return err


@receiver(post_delete)
def delete_tags(sender, **kwargs):
    """
    Delete the tags pointing to an object.
    """
    try:
        obj = kwargs.get('instance')
        tags = Tag.get_tags(obj)
        tags.delete()
    except AttributeError:
        pass
