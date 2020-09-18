from django import forms
from .models import BlogPost, Comment, Category, Subscribe, NewsLetter

choices = Category.objects.all().values_list('category_name','category_name')

choice_list =[]
for choice in choices:
    choice_list.append(choice)

class NewPostCreateForm(forms.ModelForm):
    img_url = forms.CharField(required=True)
    class Meta:
        model = BlogPost
        fields = '__all__'
        exclude = ['slug','snippet_image']
        widgets = {
            'category': forms.Select(choices=choice_list),
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}),
            'snippet_img_url': forms.TextInput(attrs={'class':'form-control','placeholder':'Type Image URL '}),
            'snippet': forms.TextInput(attrs={'class':'form-control md-textarea','placeholder':'Snippet text'})
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']
class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(required=True, widget= forms.Textarea)
class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['subscribers']
class NewslettertForm(forms.ModelForm):
    class Meta:
        model= NewsLetter
        fields = "__all__"
        exclude =['email_pics']

