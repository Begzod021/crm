from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.cache import never_cache


def remember_me_login (
    request,
    template_name = 'registration/login.html',
    redirect_field_name = REDIRECT_FIELD_NAME,
    ):

    """
    Based on code cribbed from django/trunk/django/contrib/auth/views.py
    
    Displays the login form with a remember me checkbox and handles the login
    action.
    
    """
    
    from django.conf import settings
    from django.contrib.sites.models import RequestSite, Site
    from django.http import HttpResponseRedirect
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    
    from remember_me.forms import AuthenticationRememberMeForm
    
    redirect_to = request.REQUEST.get ( redirect_field_name, '' )
    
    if request.method == "POST":
    
        form = AuthenticationRememberMeForm ( data = request.POST, )
        
        if form.is_valid ( ):
        
            # Light security check -- make sure redirect_to isn't garbage.
            
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
            
                redirect_to = settings.LOGIN_REDIRECT_URL
                
            if not form.cleaned_data [ 'remember_me' ]:
            
                request.session.set_expiry ( 0 )
                
            from django.contrib.auth import login
            
            login ( request, form.get_user ( ) )
            
            if request.session.test_cookie_worked ( ):
            
                request.session.delete_test_cookie ( )
                
            return HttpResponseRedirect ( redirect_to )
            
    else:
    
        form = AuthenticationRememberMeForm ( request, )
        
    request.session.set_test_cookie ( )
    
    if Site._meta.installed:
    
        current_site = Site.objects.get_current ( )
        
    else:
    
        current_site = RequestSite ( request )
        
    return render_to_response (
            template_name,
            {
                'form': form,
                redirect_field_name: redirect_to,
                'site': current_site,
                'site_name': current_site.name,
                },
            context_instance = RequestContext ( request ),
            )
remember_me_login = never_cache ( remember_me_login )
