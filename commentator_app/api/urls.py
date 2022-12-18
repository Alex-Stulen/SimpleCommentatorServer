from django.urls import path, include

urlpatterns = [
    path('v1/', include('commentator_app.api.v1.urls')),
]
