from django.urls import path, include

urlpatterns = [
    path('api/', include('commentator_app.api.urls')),
]
