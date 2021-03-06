feincms-forms-builder
=====================

Integrate django-forms-builder_ into FeinCMS_.

Requirements:
-------------

* FeinCMS
* django-forms-builder
* crispy-forms (optional for rendering forms inside page)

Installation
------------

::

  pip install -e git+https://github.com/bmihelac/feincms-forms-builder.git#egg=feincms-forms-builder


Add required applications to ``settings.py``::

    INSTALLED_APPS = (
        ...
        'feincms',
        'feincms.module.page',
    
        'crispy_forms',
        'forms_builder.forms',
        'forms_builder_integration',
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
    
.. _django-forms-builder: https://github.com/stephenmcd/django-forms-builder

.. _FeinCMS: https://github.com/feincms/feincms
