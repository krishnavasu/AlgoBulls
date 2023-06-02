from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.serializers import jwt_encode_handler ,jwt_decode_handler
# Create your views here.
from django.utils.translation import gettext as _
from rest_framework import serializers, viewsets,permissions
from .models import Todo, User,Tag
from .authentication import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
class TodoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length = 255)
    class Meta:
        model = User
        fields =("name","email","password")
    def validate_password(self, password):
        if password:
            if len(password) < 4:
                raise serializers.ValidationError(
                    "Password must be at least 4 characters long!"
                )
        return password
class TodoItemViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = [IsAuthenticated,]
    pagination_class = TodoPagination
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(owner=user)

    def perform_create(self, serializer):
        tags_data = self.request.data.get('tag', [])
        todo = serializer.save(owner=self.request.user)
        self._process_tags(todo, tags_data,owner=self.request.user)

    def perform_update(self, serializer):
        tags_data = self.request.data.get('tag', [])
        todo = serializer.save()
        self._process_tags(todo, tags_data,owner=self.request.user)

    def _process_tags(self, todo, tags_data,owner):
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name,owner=owner)

            tags.append(tag)
            
        todo.tags.set(tags)

def jwt_payload_handler(user):
    return {
        "id" :user.pk,
        "email":user.email,
        "name":user.name,
    }

class RegistrationView(APIView):
    def post(self,request):
        data = request.data
        print("akash",data)
        form = RegisterSerializer(data=data)
        if form.is_valid():
            name = data['name']
            email = data['email']
            password = data['password']
            user = User(email = email,name=name,)
            # user.history.set(None)
            user.set_password(password)
            user.save()
            return Response(
                    {"error": False, "message": "User created Successfully."},
                    status=status.HTTP_200_OK,
                )
        return Response({'error': True, 'errors': form.errors},
                        status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
        def post(self,request):
            data =  request.data
            email = data["email"]
            password = data["password"]
            errors = {}
            if not email:
                errors['email'] = ['This field is required']
            if not password:
                errors['password'] = ['This field is required']
            if errors:
                return Response({'error': True, 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(email=email).first()
            if not user:
                return Response(
                    {"error": True, "errors": "user not avaliable in our records"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if user.check_password(password):
                payload = jwt_payload_handler(user)
                response_data = {
                    "token": jwt_encode_handler(payload),
                    "error": False,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            password_field = "doesnot match"
            msg = _("Email and password {password_field}")
            msg = msg.format(password_field=password_field)
            return Response(
                {"error": True, "errors": msg},
                status=status.HTTP_400_BAD_REQUEST,
            )

class Tags(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated,]
    # pagination_class = TodoPagination
    def get_queryset(self):
        user = self.request.user
        print("users : ",user)
        return Todo.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)    

class DecodeToke(APIView):
    def post(self,request):
        # print("token :",request.headers['Authorization'])
        token = request.headers['Authorization'].split()[1]
        x = jwt_decode_handler(token)
        print()
        # print(x["id"])
        return Response({"mes":"success"},status=status.HTTP_200_OK)