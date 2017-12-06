from django.shortcuts import render
from .models import posts

# Create your views here.
def post(request):
    data = posts.objects.all()

    #print(data[0].query)
    contact=[]
    for i,t in enumerate(data):
        temp=[]
        temp.append(t.query)
        temp.append(t.description)
        temp.append(t.id)
        contact.append(temp)

    return render(request, 'post/posts.html',{'page':"post",'contact':contact})

def form(request):
    return render(request, 'post/form.html',{'page':"form"})

def sub(request):
    q=request.POST['subject']
    m=request.POST['Message']

    u=request.user
    if u.is_active:
        #print("adbkx")
        p=posts(user=u,query=q,description=m)
        p.save()



    return render(request, '/post/posts.html')

def detail(request,pk):
    post=posts(id=pk)
    p=[]
    temp=[]
    temp.append(post.id)
    temp.append(post.query)
    print (post.query)
    temp.append(post.description)
    p.append(temp)
    return render(request, 'post/print.html', {'page': p})