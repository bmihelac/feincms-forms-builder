from django.contrib import admin
from django.utils.translation import ungettext, ugettext_lazy as _

from forms_builder.forms.admin import FormAdmin as BaseFormAdmin
from forms_builder.forms.models import Form, Field


HIDDEN_FIELDS = ('publish_date', 'expiry_date',)

class FieldAdmin(admin.TabularInline):
    model = Field
    extra = 0

class FormAdmin(BaseFormAdmin):
    inlines = (FieldAdmin,)
    exclude = HIDDEN_FIELDS
    list_display = ("title", "email_copies", "total_entries")
    list_editable = ()
    list_filter = ()
    fieldsets = [
        (None, {"fields": ("title",
            "intro", "button_text", "response")}),
        (_("Email"), {"fields": ("send_email", "email_from", "email_copies",
            "email_subject", "email_message")}),]


admin.site.unregister(Form)
admin.site.register(Form, FormAdmin)
