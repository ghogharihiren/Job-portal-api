from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import*
from .serializers import*
from rest_framework.generics import*
from django.contrib.auth import authenticate,login
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import*
from rest_framework import status
import random
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.core.mail import send_mail

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
@api_view(['GET'])
def index(request):
    api_url={
        '':'index/',
        'create':'/create/',
        'login':'/login/',
        'hr-list':'/hr-list/',
        'edit-hr':'/edit-hr/id',
        'delete-hr':'/delete-hr/id',
        'edit-user':'/edit-user/',
        'add-job':'/add-job/',
        'my-job':'/my-job/',
        'edit-post':'/edit-post/id',
        'delete-post/':'/delete-post/id',
        'mypostapplication':'/mypostapplication/id',
        'forgot-password':'/forgot-password/'
    }    
    return Response(api_url)

class Createuser(GenericAPIView):
    serializer_class=UsercreateSerializer
    queryset=User.objects.all()
    
    def post(self,request):
        serializer=UsercreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer
    queryset=User.objects.all()
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                login(request,user)
                return Response({'token':token,'msg':'login Sucessfully'},status=status.HTTP_200_OK)
            else:
                return Response({'msg':"invalid email and password "},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ForgotPasswordView(GenericAPIView):
    serializer_class=ForgotPasswordSerializer
    
    def post(self,request):
        serializer=ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data.get('email')
            if User.objects.filter(email=email).exists():
                user=User.objects.get(email=email)
                password = ''.join(random.choices('qwyertovghlk34579385',k=8))
                subject="Rest Password"
                message = f"""Hello {user.email},Your New password is {password}"""
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email,]
                send_mail( subject, message, email_from, recipient_list )
                user.password=make_password(password)
                user.save()
                return Response('your new password send')
            else:
                return Response('enter your email')
        else:
            return Response('enter the valid data')
#---------------------------------------------Admin----------------------------------------------
class HrlistView(ListAPIView):
    serializer_class=UserViewSerializer
    queryset=User.objects.all()
    permission_classes =[IsAdminUser]
    
    
class EditView(GenericAPIView): 
    permission_classes =[IsAdminUser]
    queryset=User.objects.all()
    serializer_class=UserViewSerializer
    
    def get(self,request,pk):
        uid=User.objects.get(id=pk)
        serializer=UserViewSerializer(uid)
        return Response(serializer.data)
    
    def put(self,request,pk):
        uid=User.objects.get(id=pk)
        serializer=UserViewSerializer(instance=uid,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Hr profile update'},status=status.HTTP_200_OK)
        return Response({'msg':'Enter the valid data'},status=status.HTTP_404_NOT_FOUND)

class DeleteView(GenericAPIView):
    permission_classes =[IsAdminUser]
    queryset=User.objects.all()
    serializer_class=UserViewSerializer
    
    def get(self,request,pk):
        uid=User.objects.get(id=pk)
        serializer=UserViewSerializer(uid)
        return Response(serializer.data)
    
    def delete(self,request,pk):
        uid=User.objects.get(id=pk)
        if uid.role =='hr':
            uid.delete()
            return Response('HR delete')
        return Response('you can not delete admin')
#----------------------------------------------------HR----------------------------------------------
    
class UserProfileView(GenericAPIView):
    serializer_class=UserProfileSerializer
    queryset=User.objects.all()
    permission_classes =[IsAuthenticated]
    
    def get(self,request):
        uid=User.objects.get(id=request.user.id)
        serializer=UserProfileSerializer(uid)
        return Response(serializer.data)
        
    
    def put(self,request):
        uid=User.objects.get(id=request.user.id)
        serializer=UserProfileSerializer(instance=uid,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'profile update'},status=status.HTTP_200_OK)
        return Response({'msg':'Enter the valid data'},status=status.HTTP_400_BAD_REQUEST)
    

class PostjobView(GenericAPIView):
    serializer_class=AddpostSerializer
    post=JobPost.objects.all()
    permission_classes =[IsAuthenticated]
    
    def post(self,request):
        serializer=AddpostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(HR=request.user)
            return Response({'msg':'Job Post created'},status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response({'msg':'Enter the valid data'},status=status.HTTP_404_NOT_FOUND)
    

class JobViewAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobPost.objects.all()
    serializer_class = AddpostSerializer
    
    def get(self,request):
        post=JobPost.objects.filter(HR=request.user)
        serializer=AddpostSerializer(post,many=True)
        return Response(serializer.data)
    
class Editjobview(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobPost.objects.all()
    serializer_class = EditpostSerializer
    
    
    def get(self,request,pk):
        uid=JobPost.objects.get(id=pk)
        if uid.HR == request.user:
            serializer=EditpostSerializer(uid)
            return Response(serializer.data)
        return Response('this slot is not your')
        
    
    def put(self,request,pk):
        uid=JobPost.objects.get(id=pk)
        if uid.HR == request.user:
            serializer=EditpostSerializer(instance=uid,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Job Post update'},status=status.HTTP_200_OK)
            return Response({'msg':'Enter the valid data'},status=status.HTTP_404_NOT_FOUND)
        return Response('this slot is not your')
    
class Deletejobview(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobPost.objects.all()
    
    def get(self,request,pk):
        uid=JobPost.objects.get(id=pk)
        if uid.HR == request.user:
            serializer=EditpostSerializer(uid)
            return Response(serializer.data)
        return Response('this slot is not your')
            
    def delete(self,request,pk):
        uid=JobPost.objects.get(id=pk)
        if uid.HR == request.user:
            uid.delete()
            return Response('Job Post delete')
        return Response('this slot is not your')
        
class MyPostApplicationView(GenericAPIView):
    queryset = JobPost.objects.all()
    serializer_class = MyPostApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    
    def get(self,request,pk):
        job=JobPost.objects.get(id=pk)
        if job.HR == request.user:
            uid=Application.objects.filter(company_name=job)
            serializer=MyPostApplicationSerializer(uid,many=True)
            return Response(serializer.data)
        return Response('this job post is not your')
     
#----------------------------------------------------User-------------------------------------------    
    
class ApplicationView(GenericAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    
    def post(self,request):
        serializer=ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Apply successfully'},status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response({'msg':'Enter the valid deatils'},status=status.HTTP_404_NOT_FOUND)
    

    
    
   
    
    