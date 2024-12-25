from allauth.account.forms import LoginForm, SignupForm
from django import forms

from .models import CustomUser


class MySignupForm(SignupForm):
    account_type = forms.IntegerField(label="会員タイプ")
    user_name = forms.CharField(max_length=255, label="氏名")
    is_subscribed = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(MySignupForm, self).__init__(*args, **kwargs)
        # システム管理者 (3) を選択肢から除外
        valid_choices = [choice for choice in CustomUser.ACCOUNT_TYPE if choice[0] != 3]
        self.fields["account_type"].widget = forms.Select(
            choices=valid_choices, attrs={"class": "form-control"}
        )
        self.fields["user_name"].widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "任意のなまえ",
                "autocomplete": "off",
                "value": "",
            }
        )
        self.fields["email"].widget = forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
                "placeholder": "taro.samurai@example.com",
            }
        )
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"class": "form-control"}
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"class": "form-control"}
        )

    def signup(self, request, user):
        user.account_type = self.cleaned_data["account_type"]
        user.user_name = self.cleaned_data["user_name"]
        user.save()
        return user


class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
        print("MyLoginForm initialized")  # デバッグ用のプリント文
        self.fields["login"].widget = forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
                "placeholder": "メールアドレス",
            }
        )
        self.fields["password"].widget = forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "パスワード"}
        )
        self.fields["remember"].widget.attrs.update({"class": "form-check-input"})

    def clean(self):
        print("MyLoginForm clean method called")  # デバッグ用のプリント文
        cleaned_data = super().clean()
        user = self.get_user()
        print(f"clean method user: {user}")  # デバッグ用のプリント文
        return cleaned_data

    def get_user(self):
        email = self.cleaned_data.get("login")
        password = self.cleaned_data.get("password")
        from django.contrib.auth import authenticate

        user = authenticate(email=email, password=password)
        print(f"get_user: {user}")  # デバッグ用のプリント文
        return user


class UserUpdateForm(forms.ModelForm):
    new_password1 = forms.CharField(
        label="新しいパスワード",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
    )
    new_password2 = forms.CharField(
        label="新しいパスワード（確認）",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ("user_name", "account_type", "email", "username")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_name"].widget = forms.TextInput(
            attrs={"class": "form-control", "placeholder": "そらの木"}
        )
        valid_choices = [choice for choice in CustomUser.ACCOUNT_TYPE]
        self.fields["account_type"].widget = forms.Select(
            choices=valid_choices, attrs={"class": "form-control"}
        )
        self.fields["username"].required = False
        self.fields["username"].widget = forms.TextInput(
            attrs={"class": "form-control", "placeholder": "侍 太郎（任意）"}
        )
        self.fields["email"].widget = forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
                "placeholder": "taro.samurai@example.com",
            }
        )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password1 != password2:
            self.add_error("new_password2", "パスワードが一致しません。")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password1")
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "user_name",
            "email",
            "account_type",
            "is_subscribed",
            "card_number",
            "card_name",
            "expiry",
        ]
