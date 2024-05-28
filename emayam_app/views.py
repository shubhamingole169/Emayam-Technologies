
from django.shortcuts import render
from django.http import HttpResponseForbidden
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .serializers import UserSerializer, CustomTokenObtainPairSerializer

User = get_user_model()

# API views
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# Function-based views for rendering HTML pages
def login_page(request):
    return render(request, 'emayam_app/login.html')

def register_page(request):
    return render(request, 'emayam_app/register.html')

def dashboard_page(request):
    return render(request, 'emayam_app/dashboard.html')

def admin_page(request):
    return render(request, 'emayam_app/admin.html')

def editor_page(request):
    return render(request, 'emayam_app/editor.html')

def viewer_page(request):
    return render(request, 'emayam_app/viewer.html')

def home(request):
    return render(request, 'emayam_app/home.html')

@login_required
def view_content(request):
    content = "This is some viewable content."
    if request.user.role not in ['admin', 'editor', 'viewer']:
        return HttpResponseForbidden("You do not have permission to view this page.")
    return render(request, 'emayam_app/view_content.html', {'content': content})

@login_required
def edit_content(request):
    if request.user.role not in ['admin', 'editor']:
        return HttpResponseForbidden("You do not have permission to edit this content.")
    
    content = "This is some editable content."
    if request.method == "POST":
        content = request.POST.get('content')
        # Save the content to the database
    return render(request, 'emayam_app/edit_content.html', {'content': content})

# This view should now render an HTML template
def api_root(request):
    return render(request, 'emayam_app/api_root.html')
