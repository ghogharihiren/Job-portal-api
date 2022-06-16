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
        'edit-user':'/edit-user/id',
        'add-job':'/add-job/',
        'my-job':'/my-job/',
        'edit-post':'/edit-post/id',
        'delete-post/':'/delete-post/id',
        'mypostapplication':'/mypostapplication/id'
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
        uid.delete()
        return Response('HR delete')
#----------------------------------------------------HR----------------------------------------------
    
class UserProfileView(GenericAPIView):
    serializer_class=UserProfileSerializer
    queryset=User.objects.all()
    permission_classes =[IsAuthenticated]
    
    def get(self,request,pk):
        uid=User.objects.get(id=pk)
        serializer=UserProfileSerializer(uid)
        return Response(serializer.data)
        
    
    def put(self,request,pk):
        uid=User.objects.get(id=pk)
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
            serializer.save()
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
        serializer=EditpostSerializer(uid)
        return Response(serializer.data)
    
    def put(self,request,pk):
        uid=JobPost.objects.get(id=pk)
        serializer=EditpostSerializer(instance=uid,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Job Post update'},status=status.HTTP_200_OK)
        return Response({'msg':'Enter the valid data'},status=status.HTTP_404_NOT_FOUND)
    
class Deletejobview(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobPost.objects.all()
    
    def get(self,request,pk):
        uid=JobPost.objects.get(id=pk)
        serializer=EditpostSerializer(uid)
        return Response(serializer.data)
    
    def delete(self,request,pk):
        uid=JobPost.objects.get(id=pk)
        uid.delete()
        return Response('Job Post delete')
    
class MyPostApplicationView(GenericAPIView):
    queryset = JobPost.objects.all()
    serializer_class = MyPostApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    
    def get(self,request,pk):
        job=JobPost.objects.get(id=pk)
        uid=Application.objects.filter(company_name=job)
        serializer=MyPostApplicationSerializer(uid,many=True)
        return Response(serializer.data)
     
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
    

    
    
   
    
    