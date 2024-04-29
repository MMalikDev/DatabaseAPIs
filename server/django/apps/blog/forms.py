from django import forms


class ArticleForm(forms.Form):
    form_template_name = "components/snippets/form.html"
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
