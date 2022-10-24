from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .file_handler import *
from .models import Book
from .models import Catalog
from .models import Store
from .models import Review
from .forms import NewUserForm, BookForm

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
    return render(request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect(request.POST.get('next', '/'))
            else:
                messages.info(request,"Invalid username or password.")
        else:
            messages.info(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect(request.META['HTTP_REFERER'])

@login_required
def del_review(request, rid):
    rev = Review.objects.get(id=rid)
    uid = rev.book.uid
    rev.delete()
    messages.info(request, "Review deleted.")

    return redirect(f"/book/{uid}#reviews")

@login_required
def post_review(request, uid):
    book = get_object_or_404(Book, pk=uid)

    get_text = request.POST.get('text')
    get_user = request.user

    rev = Review(author=get_user, book=book, text=get_text.strip())

    try:
        rev.full_clean()
    except ValidationError as e:
        messages.info(request, e.messages[0])
    else:
        rev.save()
        messages.success(request, "Your review has been successfully published!")

    return redirect(f"/book/{uid}#reviews")

def catalog(request):
    books = Book.objects.get_queryset().order_by('-uid')
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

def update_catalog(uid):
    book = Book.objects.get(pk=uid)

    for st in Store.objects.all():
        Catalog.objects.create(count=0, book=book, store=st)

@user_passes_test(lambda u: u.is_superuser)
def new_book(request):
    form = BookForm()
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                book = form.save(commit=False)
                book.uid = Book.objects.latest('uid').uid + 1

                book.validate_book()

                if len(request.FILES) > 0:
                    if not "jpeg" in request.FILES['cover'].content_type or not handle_uploaded_cover(request.FILES['cover'], book.uid, book.title, book.author):
                        raise ValidationError("Failed to upload book cover.")

                if len(request.FILES) > 1:
                    if not "epub" in request.FILES['ebook_file'].content_type or not handle_uploaded_ebook(request.FILES['ebook_file'], book.uid):
                        raise ValidationError("Failed to upload ebook file.")
                    else:
                        book.ebook = True

            except ValidationError as e:
                messages.info(request, e.messages[0])
            else:
                book.save()
                messages.success(request, "New book has been successfully published!")
                update_catalog(book.uid)
                return redirect(f"/book/{book.uid}")
        else:
            messages.info(request, "Invalid data")

    context = {
        'book_form': form
    }

    context.update(base_context())
    return render(request, "book_form.html", context)

@user_passes_test(lambda u: u.is_superuser)
def edit_book(request, uid):
    book = get_object_or_404(Book, uid=uid)
    on_change = (book.title, book.author)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            try:
                book = form.save(commit=False)
                book.validate_book()

                print(book.title)

                if len(request.FILES) > 0:
                    if not "jpeg" in request.FILES['cover'].content_type or not handle_uploaded_cover(request.FILES['cover'], book.uid, book.title, book.author):
                        raise ValidationError("Failed to upload book cover.")
                elif on_change != (book.title, book.author):
                    update_cover_title(uid, book.title, book.author)

                if len(request.FILES) > 1:
                    if not "epub" in request.FILES['ebook_file'].content_type or not handle_uploaded_ebook(request.FILES['ebook_file'], book.uid):
                        raise ValidationError("Failed to upload ebook file.")
                    else:
                        book.ebook = True
                

            except ValidationError as e:
                messages.info(request, e.messages[0])
            else:
                book.save()
                messages.success(request, "Book has been successfully updated!")
                update_catalog(book.uid)
                return redirect('book', uid=book.uid)
    else:
        form = BookForm(instance=book)

    context = {
        'book_form': form
    }

    context.update(base_context())
    return render(request, 'book_edit.html', context)

@user_passes_test(lambda u: u.is_superuser)
def change_stock(request, uid):
    if request.method == "POST":
        amount = int(request.POST.get("amount"))
        stock = Catalog.objects.get(id=uid)
        if amount < 0:
            messages.info(request, "Invalid amount.")
        else:
            stock.count = amount
            stock.save()

    return redirect(f"/book/{stock.book.uid}#stock")

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


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)