from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


from .models import Book
from .models import Catalog
from .models import Store
from .models import Review
from .forms import NewUserForm

def base_context():
    stores = Store.objects.all()

    return {'base_stores': stores}

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/")
        messages.info(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.info(request,"Invalid username or password.")
        else:
            messages.info(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect(request.META['HTTP_REFERER'])

def del_review(request, rid):
    rev = Review.objects.get(id=rid)
    uid = rev.book.uid
    rev.delete()
    messages.info(request, "Review deleted.")

    return redirect(f"/book/{uid}#reviews")


def post_review(request, uid):
    book = get_object_or_404(Book, pk=uid)

    get_text = request.POST.get('text')
    get_user = request.user

    if len(get_text) < 100 or len(get_text) > 2000:
        messages.info(request, "Your review does not meet the size criteria.")
    else:
        get_text=get_text.strip()
        Review.objects.create(author=get_user, book=book, text=get_text)
        messages.success(request, "Your review has been successfully published!")

    return redirect(f"/book/{uid}#reviews")

def catalog(request):
    books = Book.objects.all()
    get_query = request.GET.get('q')
    get_subject = request.GET.get('subject')
    get_sort = request.GET.get('sort')

    if get_query:
        books = Book.objects.filter(Q(title__icontains=get_query) |
            Q(author__icontains=get_query)).distinct()
    if get_sort:
        if get_sort == "1":
            books = books.all().order_by('title')
        elif get_sort == "2":
            books = books.all().order_by('author')
        elif get_sort == "3":
            books = books.all().order_by('price')
    if get_subject:
        books = books.all().filter(subject__contains=[get_subject])


    paginator = Paginator(books, 20)
    page = request.GET.get('page')

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)


    stores = Store.objects.all()

    context = {
        'subjects': Book.subjects(),
        'books': books,
        'stores': stores
    }

    context.update(base_context())
    return render(request, 'catalog.html', context)

def book(request, uid):
    book = get_object_or_404(Book, pk=uid)

    stock = Catalog.objects.filter(book=book).order_by('-count')

    reviews = Review.objects.filter(book=book).order_by('-created_date')

    context = {
        'stock': stock,
        'book': book,
        'reviews': reviews,
    }

    context.update(base_context())
    return render(request, 'book.html', context)

def store(request, sid):
    store = get_object_or_404(Store, pk=sid)

    context = {
        'store': store
    }

    context.update(base_context())
    return render(request, 'store.html', context)

def about(request):
    context = {}
    context.update(base_context())
    return render(request, 'about.html', context)