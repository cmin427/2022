from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User,foodmodel,user_history
from menufriend_algorithm import mf_main
from other_functions_2 import make_diet,menu_title_by_day
import csv
import pandas as pd
import random
days = ['sun','mon','tue','wed','thu','fri','sat']
# Create your views here.
def index(request):
    context = {}
    return render(request, 'index.html', context)


def login_view(request):
    context={}
    if request.method =="POST":
        if request.POST["username"] and request.POST['password']:

            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

            if user is not None:
                Users_pk = user.pk
                print("인증성공")
                            
                Users = User.objects.get(pk=Users_pk)
                hist = user_history.objects.get(user_num=Users_pk)
                Users_1 = Users.견과류
                Users_1 = float(Users_1)
                Users_2 = Users.곡물전분류
                Users_2 = float(Users_2)
                Users_3 = Users.기타
                Users_3 = float(Users_3)
                Users_4 = Users.김치류
                Users_4 = float(Users_4)
                Users_5 = Users.난류
                Users_5 = float(Users_5)
                Users_6 = Users.면류
                Users_6 = float(Users_6)
                Users_7 = Users.버섯류
                Users_7 = float(Users_7)
                Users_8 = Users.유제품
                Users_8 = float(Users_8)
                Users_9 = Users.육류
                Users_9 = float(Users_9)
                Users_10 = Users.조리가공품류
                Users_10 = float(Users_10)
                Users_11 = Users.조미료
                Users_11 = float(Users_11)
                Users_12 = Users.채소류
                Users_12 = float(Users_12)
                Users_13 = Users.해산물
                Users_13 = float(Users_13)
                
                user_1 = [{'견과류': Users_1, '곡물전분류': Users_2, '기타': Users_3, '김치류': Users_4, '난류': Users_5, '면류': Users_6, '버섯류': Users_7, 
                '유제품': Users_8, '육류': Users_9, '조리가공품류': Users_10, '조미료': Users_11, '채소류': Users_12, '해산물': Users_13},[]]
                #print(f'mf_1500{user_1[1]}:',mf_main(1,user_1,1,10))
                mf_main_10 = mf_main(1, user_1, 1, 6)
                
                df = pd.read_csv("./mfd.csv", encoding = 'utf-8')
                df1 = df.loc[:,'title']
                menu_index1 = mf_main_10[0]
                title1 = df1.loc[mf_main_10[0]]
                menu_index2 = mf_main_10[1]
                title2 = df1.loc[mf_main_10[1]]
                menu_index3 = mf_main_10[2]
                title3 = df1.loc[mf_main_10[2]]
                menu_index4 = mf_main_10[3]
                title4 = df1.loc[mf_main_10[3]]
                menu_index5 = mf_main_10[4]
                title5 = df1.loc[mf_main_10[4]]
                menu_index6 = mf_main_10[5]
                title6 = df1.loc[mf_main_10[5]]
                context = {'Users':Users,'mf_main_10':mf_main_10,
                'menu_index1':menu_index1,'menu_index2':menu_index2,'menu_index3':menu_index3,
                'menu_index4':menu_index4,'menu_index5':menu_index5,'menu_index6':menu_index6,
                'title1':title1,'title2':title2,'title3':title3,'title4':title4,'title5':title5,'title6':title6}
                #'mf_main_10_0':mf_main_10[0], 'mf_main_10_1':mf_main_10[1], 'mf_main_10_2':mf_main_10[2], 'mf_main_10_3':mf_main_10[3], 'mf_main_10_4':mf_main_10[4], 'mf_main_10_5':mf_main_10[5], 'mf_main_10_6':mf_main_10[6], 'mf_main_10_7':mf_main_10[7], 'mf_main_10_8':mf_main_10[8], 'mf_main_10_9':mf_main_10[9]

                
                login(request, user)
            else:
                print("인증실패")
                context['error'] = '아이디와 비밀번호를 다시 확인해주세요.'
    
        else:
            context['error'] = '아이디와 비밀번호를 모두 입력해주세요.'
    
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def signup(request):
    context = {}


    if request.method =="POST":
        if (request.POST['username'] and request.POST['password'] and request.POST['password'] == request.POST['password2']):
            
            username = request.POST["username"]
            name = request.POST["name"]
            password = request.POST["password"]
            email = request.POST["email"]
            height = request.POST["height"]
            weight = request.POST["weight"]
            gender = request.POST["gender"]
            곡물전분류 = request.POST["곡물전분류"]
            김치류 = request.POST["김치류"]
            난류 = request.POST["난류"]
            면류 = request.POST["면류"]
            버섯류 = request.POST["버섯류"]
            유제품 = request.POST["유제품"]
            육류 = request.POST["육류"]
            조리가공품류 = request.POST["조리가공품류"]
            채소류 = request.POST["채소류"]
            해산물 = request.POST["해산물"]
            견과류 = request.POST["견과류"]


            user = User.objects.create_user(username, email, password)
            print(user.pk)
            user.name = name
            user.height = height
            user.weigth = weight
            user.gender = gender
            user.곡물전분류 = 곡물전분류
            user.김치류 = 김치류
            user.난류 = 난류
            user.면류 = 면류
            user.버섯류 = 버섯류
            user.유제품 = 유제품
            user.육류 = 육류
            user.조리가공품류 = 조리가공품류
            user.채소류 = 채소류
            user.해산물 = 해산물
            user.기타 = 1
            user.조미료 = 1
            user.견과류 = 견과류
            user_history.objects.create(
                user_num = user.pk,
                food_1 = '-1',
            )

                        
            user.save()
        
            return redirect("index")

        else:
            context['error'] = '아이디와 비밀번호를 다시 확인해주세요.'

    return render(request, 'signup.html', context)


def recipe1(request):
    return render(request, 'recipe1.html')


def recipe_1(request,menu_index,Users_pk):
    if request.method == "POST":
        print('recipe_1, POST')
    Users = User.objects.get(pk=Users_pk)
    context = {}
    df = pd.read_csv("./mfd.csv")
    title = df.loc[menu_index,'title']
    ingre = df.loc[menu_index,'raw_ingre']
    step = df.loc[menu_index,'steps']
    context = {'title':title,'ingre':ingre,'step':step,'menu_index':menu_index,'Users_pk':Users_pk}
    if request.method =="POST":
        return redirect('recommend',context)
    return render(request, 'recipe_1.html',context)

def recipe_2(request):
    return render(request, 'recipe_2.html')

def recipe_3(request):
    return render(request, 'recipe_3.html')

def recipe_4(request):
    return render(request, 'recipe_4.html')

def recipe_5(request):
    return render(request, 'recipe_5.html')

def recommend(request,User_pk):
    df = pd.read_csv("./mfd.csv", encoding = 'utf-8')
    df1 = df.loc[:,'title']
    hist = user_history.objects.get(user_num=User_pk)
    Users = User.objects.get(pk=User_pk)
    if request.method == "POST":
        selected_menu = request.POST["menu_index"]
        recent_history = make_diet(hist.food_1,selected_menu,'s')
        user_history.objects.filter(user_num=User_pk).update(
            food_1=recent_history
            )
    hist = user_history.objects.get(user_num=User_pk)
    day_list = hist.food_1.split(',')
    user_hist = day_list[-1:-4:-1]
    print('user_info[1]:',user_hist)
    print('user in db:',day_list)
    day_list = [int(item) for item in day_list[1:]]
    # print('2',day_list)
    # day_list = day_list[-1:len(day_list)-8:-1]
    # print('3',day_list)
    # day_list = day_list[::-1]
    if len(day_list) < 7:
        filler = (7-len(day_list)) * [-1]
        day_list += filler
    day_sun = menu_title_by_day(df1,day_list[0])
    day_mon = menu_title_by_day(df1,day_list[1])
    day_tue = menu_title_by_day(df1,day_list[2])
    day_wed = menu_title_by_day(df1,day_list[3])
    day_thu = menu_title_by_day(df1,day_list[4])
    day_fri = menu_title_by_day(df1,day_list[5])
    day_sat = menu_title_by_day(df1,day_list[6])
    print('recent 7days:',day_list)
    print(day_sun,day_mon,day_tue,day_wed,day_thu,day_fri,day_sat)
    n = day_list[6]
    Users_1 = Users.견과류
    Users_1 = float(Users_1)
    Users_2 = Users.곡물전분류
    Users_2 = float(Users_2)
    Users_3 = Users.기타
    Users_3 = float(Users_3)
    Users_4 = Users.김치류
    Users_4 = float(Users_4)
    Users_5 = Users.난류
    Users_5 = float(Users_5)
    Users_6 = Users.면류
    Users_6 = float(Users_6)
    Users_7 = Users.버섯류
    Users_7 = float(Users_7)
    Users_8 = Users.유제품
    Users_8 = float(Users_8)
    Users_9 = Users.육류
    Users_9 = float(Users_9)
    Users_10 = Users.조리가공품류
    Users_10 = float(Users_10)
    Users_11 = Users.조미료
    Users_11 = float(Users_11)
    Users_12 = Users.채소류
    Users_12 = float(Users_12)
    Users_13 = Users.해산물
    Users_13 = float(Users_13)
    user_1 = [{'견과류': Users_1, '곡물전분류': Users_2, '기타': Users_3, '김치류': Users_4, '난류': Users_5, '면류': Users_6, '버섯류': Users_7, 
    '유제품': Users_8, '육류': Users_9, '조리가공품류': Users_10, '조미료': Users_11, '채소류': Users_12, '해산물': Users_13},user_hist]
    #print(f'mf_1500{user_1[1]}:',mf_main(1,user_1,1,10))
    mf_main_10 = mf_main(1, user_1, 1, 10)
    
    menu_index1 = mf_main_10[0]
    title1 = df1.loc[mf_main_10[0]]
    menu_index2 = mf_main_10[1]
    title2 = df1.loc[mf_main_10[1]]
    menu_index3 = mf_main_10[2]
    title3 = df1.loc[mf_main_10[2]]
    menu_index4 = mf_main_10[3]
    title4 = df1.loc[mf_main_10[3]]
    menu_index5 = mf_main_10[4]
    title5 = df1.loc[mf_main_10[4]]
    menu_index6 = mf_main_10[5]
    title6 = df1.loc[mf_main_10[5]]
    context = {'Users':Users,'n':n,
    'menu_index1':menu_index1,'menu_index2':menu_index2,'menu_index3':menu_index3,
    'menu_index4':menu_index4,'menu_index5':menu_index5,'menu_index6':menu_index6,
    'title1':title1,'title2':title2,'title3':title3,'title4':title4,'title5':title5,'title6':title6,'hist':hist,
    'day_sun':day_sun,'day_mon':day_mon,'day_tue':day_tue,'day_wed':day_wed,'day_thu':day_thu,'day_fri':day_fri,'day_sat':day_sat,}
    # if Users.is_authenticated:
    #     print(Users.is_authenticated)
    return render(request,'recommend.html',context)

def pay(request,User_pk):
    df = pd.read_csv("./mfd.csv", encoding = 'utf-8')
    df1 = df.loc[:,'title']
    hist = user_history.objects.get(user_num=User_pk)
    hist_list_ = hist.food_1.split(',')
    hist_list_ = hist_list_[len(hist_list_)-7:]
    hist_list=[]
    for hist_idx in hist_list_:
        hist_idx = int(hist_idx)
        hist_list.append(df1.loc[hist_idx])
    a = hist.food_1
    user_history.objects.filter(user_num=User_pk).update(
        food_1='-1',food_2=a,
        )
    context = {'history':hist.food_1,'hist_list':hist_list}
    return render(request,'pay.html',context)



