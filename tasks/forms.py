from django import forms
from .models import TaskAttachment, TaskComment
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskAttachmentForm(forms.ModelForm):
    class Meta:
        model = TaskAttachment
        fields = ['file']

class TaskCommentForm(forms.ModelForm):
    tagged_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Kullanıcıları Etiketle"
    )

    class Meta:
        model = TaskComment
        fields = ['content', 'tagged_users']
