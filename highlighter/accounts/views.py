from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as auth_login
from django.shortcuts import redirect,render
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from .forms import SignupForm,LoginForm
from ipware.ip import get_ip
from django.contrib.gis.geoip2 import GeoIP2

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(settings.LOGIN_URL) #default : "/accounts/login/"
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


def login(request):
    providers = []

    for provider in get_providers():

        try:
            provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)

    ip = get_ip(request)
    g = GeoIP2()
    print(ip)
    if ip is not None and ip is '127.0.0.1':

        print(g.city('218.85.133.23'))
    else:
        print('local or no ip')


    return auth_login(request,
                      authentication_form=LoginForm,
                      template_name='accounts/login_form.html',
                      extra_context={'providers': providers})

