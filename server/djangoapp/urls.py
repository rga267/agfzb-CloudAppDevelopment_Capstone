from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view

    # path for contact us view

    # path for registration

    # path for login

    # path for logout

    path(route='', view=views.get_dealerships, name='index'),
    path(route='loginPage', view=views.loginPage, name='loginPage'),
    path(route='registration', view=views.registration, name='registration'),
    path(route='logoutPage', view=views.logoutPage, name='logoutPage'),
    path(route='static', view=views.renderStatic, name='static'),
    path(route='about', view=views.aboutPage, name='about'),
    path(route='contact', view=views.contactPage, name='contact'),
    path('dealer/<str:dealer_id>/', views.get_dealer_details, name=
    'dealer_details'),
    # path for add a review view
    path('review/<str:dealer_id>', views.add_review, name='add_review'),
    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)