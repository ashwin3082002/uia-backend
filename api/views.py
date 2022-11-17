from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from utils import func
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from db.models import CitizenDetail, ManagerDetail, WorkerDetail
from django.http import JsonResponse
# Create your views here.


def home(request):
    return JsonResponse({"Message":"Hello World"})

@api_view(['POST'])
def auth(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        key = request.POST.get("key")
        if key != "thisissecret":
            return Response({"error": "Invalid key"}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=username, password=password)

        if user is not None:
            role = str(user.groups.filter().get())
            content = {"message":"success","role":role} 
            return Response(content,status=status.HTTP_202_ACCEPTED)
        else:
            content = {"message":"worng credentials"}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
    
    content = {"message":"unsuccessfull"}
    return Response(content,status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def email_send(request):
    key = request.POST.get("key")
    if key != "thisissecret":
        return Response({"error": "Invalid key"}, status=status.HTTP_401_UNAUTHORIZED)
    to_email = request.POST.get('to_email')
    subject = request.POST.get('subject')
    body = request.POST.get('body')
    if func.send_email(to_email,subject,body):
        content = {"message":"mail sent"}
        return Response(content, status=status.HTTP_200_OK)
    else:
        content = {"message":"Something Went Wrong!!"}
        return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def createuser(request):
    u_type = request.POST.get('user_type')
    key = request.POST.get("key")
    if key != "thisissecret":
        return Response({"error": "Invalid key"}, status=status.HTTP_401_UNAUTHORIZED)

    if u_type == "citizen":
        name = request.POST.get('name')
        email =  request.POST.get('email')
        phone =  request.POST.get('phone')
        state = request.POST.get('state')
        city = request.POST.get('city')
        password = request.POST.get('password')

        try:
            ud=CitizenDetail.objects.get(email=email)
        except:
            ud=None

        if ud is None:
            db_inst = CitizenDetail(
                name=name,
                email=email,
                phone=phone,
                state=state,
                city=city
            )
            db_inst.save()
            user = User.objects.create_user(email, email, password)
            user.first_name=name
            group = Group.objects.get(name='citizen')
            user.groups.add(group)
            user.save()

            return Response({"message":"user created"},status=status.HTTP_201_CREATED)
        else:
            if name:
                ud.name=name
                user = User.objects.get(username=email)
                user.first_name=name
                user.save()
            if email:
                ud.email=email
            if phone:
                ud.phone=phone
            if state:
                ud.state=state
            if city:    
                ud.city=city
            if password:
                user = User.objects.get(username=email)
                user.set_password(password)
                user.save()
            ud.save()

            return Response({"message":"user updated"},status=status.HTTP_202_ACCEPTED)

    elif u_type == 'worker':
        
        name = request.POST.get('name')
        email =  request.POST.get('email')
        phone =  request.POST.get('phone')
        state = request.POST.get('state')
        city = request.POST.get('city')
        manager = request.POST.get('manager')
        password = request.POST.get('password')

        try:
            manager_db=ManagerDetail.objects.get(email=manager)
        except:
            return Response({"message":"manager not found"},status=status.HTTP_404_NOT_FOUND)

        try:
            ud=WorkerDetail.objects.get(email=email)
        except:
            ud=None

        if ud is None:
            db_inst = WorkerDetail(
                name=name,
                email=email,
                phone=phone,
                state=state,
                city=city,
                manager=manager_db
            )
            db_inst.save()
            user = User.objects.create_user(email, email, password)
            user.first_name=name
            group = Group.objects.get(name='worker')
            user.groups.add(group)
            user.save()

            return Response({"message":"user created"},status=status.HTTP_201_CREATED)
        else:
            if name:
                ud.name=name
                user = User.objects.get(username=email)
                user.first_name=name
                user.save()
            if email:
                ud.email=email
            if phone:
                ud.phone=phone
            if state:
                ud.state=state
            if city:    
                ud.city=city
            if password:
                user = User.objects.get(username=email)
                user.set_password(password)
                user.save()
            ud.save()

            return Response({"message":"user updated"},status=status.HTTP_202_ACCEPTED)

    elif u_type == "manager":
        
        name = request.POST.get('name')
        email =  request.POST.get('email')
        phone =  request.POST.get('phone')
        state = request.POST.get('state')
        city = request.POST.get('city')
        section = request.POST.get('section')

        password = request.POST.get('password')

        try:
            ud=ManagerDetail.objects.get(email=email)
        except:
            ud=None
        

        if ud is None:
            db_inst = ManagerDetail(
                name=name,
                email=email,
                phone=phone,
                state=state,
                city=city,
                section = section
            )
            db_inst.save()
            user = User.objects.create_user(email, email, password)
            user.first_name=name
            group = Group.objects.get(name='manager')
            user.groups.add(group)
            user.save()

            return Response({"message":"user created"},status=status.HTTP_201_CREATED)
        else:
            if name:
                ud.name=name
                user = User.objects.get(username=email)
                user.first_name=name
                user.save()
            if email:
                ud.email=email
            if phone:
                ud.phone=phone
            if state:
                ud.state=state
            if city:    
                ud.city=city
            if password:
                user = User.objects.get(username=email)
                user.set_password(password)
                user.save()
            ud.save()

            return Response({"message":"user updated"},status=status.HTTP_202_ACCEPTED)

    return Response({"message":"user type not found"},status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def user_details(request):
    email = request.POST.get('email')
    key = request.POST.get("key")
    if key != "thisissecret":
        return Response({"error": "Invalid key"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = User.objects.get(username=email)
        role = str(user.groups.filter().get())
    except:
        return Response({"message":"user not found"},status=status.HTTP_404_NOT_FOUND)

    if role == "citizen":
        ud = CitizenDetail.objects.get(email=email)
        content = {"message":"success","data":{'name':ud.name,'email':ud.email,'phone':ud.phone,'state':ud.state,'city':ud.city,"role":role}}
        return Response(content,status=status.HTTP_200_OK)
    elif role == "worker":
        ud = WorkerDetail.objects.get(email=email)
        content = {"message":"success","data":{'name':ud.name,'email':ud.email,'phone':ud.phone,'state':ud.state,'city':ud.city,'manager':ud.manager.name,"role":role}}
        return Response(content,status=status.HTTP_200_OK)
    elif role == "manager":
        ud = ManagerDetail.objects.get(email=email)
        content = {"message":"success","data":{'name':ud.name,'email':ud.email,'phone':ud.phone,'state':ud.state,'city':ud.city,'section':ud.section,"role":role}}
        return Response(content,status=status.HTTP_200_OK)
    return Response({"message":"failed"},status=status.HTTP_400_BAD_REQUEST)
