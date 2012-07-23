from django.db import models
from django.template import Context, RequestContext, Template
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from forms_builder.forms.models import Form
from forms_builder.forms.forms import FormForForm
from forms_builder.forms.fields import FILE
from forms_builder.forms.signals import form_invalid, form_valid


def send_email_message(form, to, entry):
    """
    Render form.email_message and send it to ``to``.
    """
    subject = entry.form.email_subject or form.title
    context = Context({
        'form': form,
        })
    template = Template(entry.form.email_message)
    message = template.render(context)
    from_email = entry.form.email_from or settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [to])


def send_email_form(request, form, entry):
    """
    Render form_response template and send it to form.email_copies.
    """
    email_copies = [e.strip() for e in entry.form.email_copies.split(",")
                    if e.strip()]
    if not email_copies:
        return

    fields = []
    for field_entry in entry.fields.all():
        form_field = entry.form.fields.get(pk=field_entry.field_id)
        label = form_field.label
        value = field_entry.value
        if form_field.is_a(FILE) and value:
            url = reverse("admin:form_file", args=(field_entry.id,))
            value = mark_safe('<a href="%s">%s</a>' % (
                request.build_absolute_uri(url),
                value.split('/')[-1],
                ))
        fields.append((label, value,))

    context = {
        "fields": fields,
    }
    from_email = entry.form.email_from or settings.DEFAULT_FROM_EMAIL
    subject = entry.form.title
    message = render_to_string('forms/email_form.txt', context)
    send_mail(subject, message, from_email, email_copies)


class FormContent(models.Model):
    """
    django-forms-builder Form content type.

    Render form, send e-mail and render form response or redirects
    to given url.
    """
    form = models.ForeignKey(Form, verbose_name=_('Form'))

    template = 'content/forms/form.html'

    class Meta:
        abstract = True
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')

    def process(self, request, **kwargs):
        request_context = RequestContext(request)
        form = self.form
        args = (form, request_context,
                request.POST or None, request.FILES or None)
        form_for_form = FormForForm(*args)
        if request.method == "POST":
            if not form_for_form.is_valid():
                form_invalid.send(sender=request, form=form_for_form)
            else:
                entry = form_for_form.save()

                # send e-mail message to user
                email_to = form_for_form.email_to()
                if email_to and form.send_email:
                    send_email_message(form_for_form, email_to, entry)

                # send email to email_copies
                send_email_form(request, form_for_form, entry)

                form_valid.send(sender=request, form=form_for_form, entry=entry)

                if form.response.startswith('/') or form.response.startswith('http'):
                    return redirect(form.response)

                context = Context({
                    'form': form_for_form,
                    })
                template = Template(form.response)
                self.rendered_output = template.render(context)
                return

        context = {
                "form": form_for_form,
                }
        self.rendered_output = render_to_string(self.template, context,
                request_context)

    def render(self, **kwargs):
        return getattr(self, 'rendered_output', u'')

    def finalize(self, request, response):
        # Always disable caches if this content type is used somewhere
        response['Cache-Control'] = 'no-cache, must-revalidate'
