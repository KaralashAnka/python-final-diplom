from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import User, Address
from .serializers import UserSerializer, AddressSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create user but set as inactive
        user = serializer.save(is_active=False)
        
        # Send confirmation email
        self.send_confirmation_email(user, request)
        
        return Response({
            'message': 'Registration successful. Please check your email to confirm your account.',
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)
    
    def send_confirmation_email(self, user, request):
        """Send email confirmation to user"""
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # For demo purposes, we'll just send a simple confirmation message
        # In production, you would include a proper confirmation link
        subject = 'Confirm your email address'
        message = f'''
        Hello {user.get_full_name() or user.username},
        
        Thank you for registering! Please confirm your email address.
        
        User ID: {uid}
        Confirmation token: {token}
        
        Note: This is a demo implementation. In production, this would be a clickable link.
        '''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )


class ConfirmEmailView(APIView):
    """View to confirm email address"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        
        if not uid or not token:
            return Response(
                {'error': 'UID and token are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except Exception:
            return Response(
                {'error': 'Invalid user'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            
            # Create token for the user
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': 'Email confirmed successfully',
                'token': token.key,
                'user': UserSerializer(user).data
            })
        else:
            return Response(
                {'error': 'Invalid or expired token'},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if user and user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user': UserSerializer(user).data
                })
            elif user and not user.is_active:
                return Response(
                    {'error': 'Please confirm your email address before logging in'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            else:
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                {'error': 'Email and password required'},
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out'})
        except:
            return Response({'error': 'Error logging out'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        # Basic password reset implementation
        email = request.data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                # In a real implementation, send password reset email
                return Response({'message': 'Password reset email sent'})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Email required'}, status=status.HTTP_400_BAD_REQUEST)
