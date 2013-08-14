feincms-forms-builder
=====================

Integrate django-forms-builder into FeinCMS.

Requirements:
-------------

* FeinCMS
* django-forms-builder
* crispy-forms (optional for rendering forms inside page)

Installation
------------

Add required applications to ``settings.py``::

    INSTALLED_APPS = (
        ...
        'feincms',
        'feincms.module.page',
    
        'crispy_forms',
        'forms_builder.forms',
        'impckg.forms_builder_integration',
        ...
    )

Usage
-----

Register FormContent content type into FeinCMS Page:

::

    from forms_builder_integration.models import FormContent
    Page.create_content_type(FormContent, regions=('main',))


Templates
---------

::

    content/forms/form.htm
    forms/email_base.txt
    forms/email_form.txt
