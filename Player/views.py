from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from Player.models import User
from Player.models import Media
from Player.models import Admin
from django.http import HttpResponseRedirect
from Player.forms import DocumentForm
from django.template.context_processors import csrf
from django.template import RequestContext
import datetime
import os


# Create your views here.
class View(TemplateView):

    def index(request):
        context = RequestContext(request)
        c = {}
        c.update(csrf(request))
        return render_to_response('index.html', c, context)

    def login(request):
        if 'user' in request.session and request.session['user'] is not None:
            return HttpResponseRedirect('media.html')
        context = RequestContext(request)
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c, context)

    def validate(request):
        if 'user' in request.session and request.session['user'] is not None:
            return render_to_response('media.html')
        if request.POST.get("uname") is not None and request.POST.get("pass") is not None:
            username = request.POST.get("uname")
            password = request.POST.get("pass")
            if User.objects.filter(uname=username).exists() and User.objects.get(uname=username).password == password:
                request.session.modified = True
                request.session['user'] = username
                request.session.save()
                return HttpResponseRedirect('media.html')
            else:
                context = RequestContext(request)
                c = {}
                c.update(csrf(request))
                return render_to_response('login.html', c, context)
        else:
            context = RequestContext(request)
            c = {}
            c.update(csrf(request))
            return render_to_response('login.html', c, context)

    def upload_media(request):
        if 'user' in request.session and request.session['user'] is not None:
            if request.FILES['file-upload'] is not None:
                uname = User.objects.get(uname=request.session['user'])
                up_date = datetime.datetime.now()
                mr_file = request.FILES['file-upload']
                fname = mr_file.name
                if len(fname)>50:
                    fname=fname[:50]
                media = Media(uname=uname, up_date=up_date, f_name=fname, file=mr_file)
                media.save()
                return HttpResponseRedirect('upload.html')
            else:
                return HttpResponseRedirect('upload.html')
            return render(request, 'upload.html', {})
        context = RequestContext(request)
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c, context)

    def media_html(request):
        if 'user' in request.session and request.session['user'] is not None:
            user=request.session['user']
        else:
            user="Guest"
        media = Media.objects.all().order_by('up_date')
        return render(request, 'media.html', {'media': media, 'user':user})

    def gallery_html(request):
        context = RequestContext(request)
        c = {}
        c.update(csrf(request))
        if 'user' in request.session and request.session['user'] is not None:
            umedia = Media.objects.filter(uname=request.session['user'])
            return render(request, 'gallery.html', {'umedia': umedia, 'user': request.session['user']})
        return render_to_response('login.html', c, context)

    def logout(request):
        request.session.modified = True
        if 'user' in request.session and request.session['user'] is not None:
            if 'yes' in request.GET:
                # sess = request.session.pop('user')
                # del request.session['user']
                request.session.flush()

            elif 'no' in request.GET:
                return HttpResponseRedirect('media.html')
                # return HttpResponseRedirect('login.html?msg="no logout"')
        if 'admin' in request.session and request.session['admin'] is not None:
            if 'yes' in request.GET:
                # del request.session['admin']
                request.session.flush()
            else:
                return HttpResponseRedirect('admin_gallery.html')
        context = RequestContext(request)
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c, context)
        # return HttpResponseRedirect('login.html')

    def logout_html(request):
        if 'user' in request.session:
            if request.session['user'] is not None:
                return render(request, 'logout.html', {'user': request.session['user']})
        if 'admin' in request.session:
            if request.session['admin'] is not None:
                return render(request, 'logout.html', {'user': request.session['admin']})
        context = RequestContext(request)
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c, context)

    def f_delete(request):
        if 'user' in request.session and request.session['user'] is not None:
            f = request.GET['delete_f']
            media=Media.objects.get(id=f)
            fpath=media.file.path
            media.delete()
            os.remove(fpath)
            return HttpResponseRedirect('gallery.html')
        if 'admin' in request.session and request.session['admin'] is not None:
            f = request.GET['delete_f']
            Media.objects.filter(id=f).delete()
            return HttpResponseRedirect('admin_gallery.html')

        context = RequestContext(request)
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c, context)

    def admin_login(request):
        if 'admin' in request.session and request.session['admin'] is not None:
            HttpResponseRedirect('admin_gallery.html')
        context = RequestContext(request)
        c = {}
        c.update(csrf(request))
        return render_to_response('adminlogin.html', c, context)

    def admin_validate(request):
        if 'admin' in request.session and request.session['admin'] is not None:
            return HttpResponseRedirect('admin_gallery.html')
        if request.POST.get("uname") is not None and request.POST.get("pass") is not None:
            username = request.POST.get('uname')
            password = request.POST.get('pass')
            if Admin.objects.filter(uname=username).exists() and Admin.objects.get(uname=username).password == password:
                request.session.modified = True
                admin = 'admin_'
                admin = admin + username
                request.session['admin'] = admin
                request.session.save()
                return HttpResponseRedirect('admin_gallery.html')
            else:
                context = RequestContext(request)
                c = {}
                c.update(csrf(request))
                return render_to_response('adminlogin.html', c, context)
        else:
            context = RequestContext(request)
            c = {}
            c.update(csrf(request))
            return render_to_response('adminlogin.html', c, context)

    def admin_gallery(request):
        context = RequestContext(request)
        c = {}
        c.update(csrf(request))
        if 'admin' in request.session and request.session['admin'] is not None:
            media = Media.objects.all().order_by('up_date')
            return render(request, 'admin_gallery.html', {'media': media})
        return render_to_response('adminlogin.html', c, context)

    def admin_delete(request):
        if 'admin' in request.session and request.session['admin'] is not None:
            f = request.POST['delete_f']
            media = Media.objects.get(id=f)
            fpath = media.file.path
            media.delete()
            os.remove(fpath)
            return HttpResponseRedirect('admin_gallery.html')
        context = RequestContext(request)
        c = {}
        c.update(csrf(request))
        return render_to_response('adminlogin.html', c, context)

    def register(request):
        if 'user' in request.session and request.session['user'] is not None:
            return HttpResponseRedirect('media.html')
        uname = request.POST['uname']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        phone = request.POST['phone']
        country = request.POST['country']
        address = request.POST['address']
        city = request.POST['city']
        zip = request.POST['zip']
        bio = request.POST['bio']
        email1 = request.POST['email-1']
        email2 = request.POST['email-2']
        password1 = request.POST['password']
        password2 = request.POST['password_confirmation']
        isExist = User.objects.filter(uname=uname).count()
        if isExist != 0:
            return render(request, 'registration.html', {'msg': 'username already exist... please try with another'})
        if len(zip) < 6:
            return render(request, 'registration.html', {'msg': 'please enter valid zip code'})
        if email1 != email2:
            return render(request, 'registration.html', {'msg': 'Confirm email and try again...'})
        if password1 != password2:
            return render(request, 'registration.html', {'msg': 'Confirm password and try again...'})
        newuser = User(uname=uname, fname=fname, lname=lname, phone=phone, country=country, address=address, city=city,
                       zip=zip, bio=bio, email=email1, password=password1)
        newuser.save()
        # User.objects.create(uname=uname, fname=fname, lname=lname, phone=phone, country=country, address=address,city=city, zip=zip, bio=bio, email=email1, password=password1)

        context = RequestContext(request)
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c, context)

    def register_html(request):
        if 'user' in request.session and request.session['user'] is not None:
            return HttpResponseRedirect('media.html')
        return render(request, 'registration.html', {})

    def cust_users(request):
        if 'admin' in request.session and request.session['admin'] is not None:
            users = User.objects.all()
            return render(request, 'displayusers.html', {'users': users})
        context = RequestContext(request)
        c = {}
        c.update(csrf(request))
        return render_to_response('adminlogin.html', c, context)

    def del_user(request):
        if 'admin' in request.session and request.session['admin'] is not None:
            f = request.GET['delete_u']
            user=User.objects.filter(uname=f)
            files=Media.objects.filter(uname=f)
            for fl in files:
                fpath = fl.file.path
                fl.delete()
                os.remove(fpath)
            user.delete()
            return HttpResponseRedirect('displayusers.html')
        context = RequestContext(request)
        c = {}
        c.update(csrf(request))
        return render_to_response('adminlogin.html', c, context)

    def play(request):
        context = RequestContext(request)
        c = {}
        c.update(csrf(request))
        if 'user' in request.session and request.session['user'] is not None:
            f = request.POST['play_f']
            file = Media.objects.get(id=f)
            #media = Media.objects.all().order_by('up_date')
            if 'media_page' in request.POST:
                return render(request, 'media.html', {'file': file, 'c': c, 'context': context})
            elif 'gallery_page' in request.POST:
                return render(request, 'gallery.html', {'file': file, 'c': c, 'context': context})
        if 'admin' in request.session and request.session['admin'] is not None:
            f = request.POST['play_f']
            file = Media.objects.get(id=f)
            return render(request, 'admin_gallery.html', {'file': file, 'c': c, 'context': context})
        return render_to_response('login.html', c, context)

    def about_html(request):
        return render_to_response('about.html')

    def contact_html(request):
        return render_to_response('contact.html')

    def upload_html(request):
        if 'user' in request.session and request.session['user'] is not None:
            context = RequestContext(request)
            c = {}
            c.update(csrf(request))
            return render_to_response('upload.html', c, context)
        else:
            context = RequestContext(request)
            c = {}
            c.update(csrf(request))
            return render_to_response('login.html', c, context)

    def search(request):
        if 'user' in request.session and request.session['user'] is not None:
            if 'data' in request.GET:
                if request.GET['data'] is not None:
                    data = request.GET['data']
                    media = []
                    if 'media_page' in request.GET:
                        allmedia = Media.objects.order_by('up_date')
                        for some in allmedia:
                            if data in some.f_name:
                                media.append(some)
                        return render(request, 'media.html', {'media': media, 'user': request.session['user']})
                    elif 'gallery_page' in request.GET:
                        allmedia = Media.objects.filter(uname=request.session['user']).order_by('up_date')
                        for some in allmedia:
                            if data in some.f_name:
                                media.append(some)
                        return render(request, 'gallery.html', {'umedia': media, 'user': request.session['user']})
                else:
                    return HttpResponseRedirect('media.html')
            else:
                return HttpResponseRedirect('media.html')

    def sort(request):
        if 'sort' in request.POST:
            if request.POST['sort'] is not None:
                sort = request.POST['sort']
                if 'media_page' in request.POST:
                    page='media'
                elif 'gallery_page' in request.POST:
                    page='gallery'
                if page=='media':
                    if sort == 'byAscName':
                        media = Media.objects.order_by('f_name')
                    elif sort == 'byDscName':
                        media = Media.objects.order_by('-f_name')
                    elif sort == 'byAscDate':
                        media = Media.objects.order_by('up_date')
                    elif sort == 'byDscDate':
                        media = Media.objects.order_by('-up_date')
                    else:
                        HttpResponseRedirect('media.html?msg="Else"')
                    return render(request, 'media.html', {'media': media, 'user': request.session['user']})
                if page=='gallery':
                    if sort == 'byAscName':
                        media = Media.objects.filter(uname=request.session['user']).order_by('f_name')
                    elif sort == 'byDscName':
                        media = Media.objects.filter(uname=request.session['user']).order_by('-f_name')
                    elif sort == 'byAscDate':
                        media = Media.objects.filter(uname=request.session['user']).order_by('up_date')
                    elif sort == 'byDscDate':
                        media = Media.objects.filter(uname=request.session['user']).order_by('-up_date')
                    else:
                        HttpResponseRedirect('gallery.html?msg="Else"')
                    return render(request, 'gallery.html', {'umedia': media, 'user': request.session['user']})
            else:
                return HttpResponseRedirect('media.html?msg="sort is none"')
        else:
            return HttpResponseRedirect('media.html?msg="sort is not in post"')

    def searchUser(request):
        if 'data' in request.GET:
            if request.GET['data'] is not None:
                data = request.GET['data']
                users = []
                allusers = User.objects.all().order_by('uname')
                for some in allusers:
                    if data in some.uname or data in some.lname or data in some.fname or data in str(some.phone) or data in some.email or data in str(some.zip) or data in some.country:
                        users.append(some)
                return render(request, 'displayusers.html', {'users': users})
            else:
                return HttpResponseRedirect('displayusers.html')
        else:
            return HttpResponseRedirect('displayusers.html')

    def sortUser(request):
        if 'sort' in request.GET:
            if request.POST['sort'] is not None:
                sort = request.POST['sort']
                if sort == 'byAscName':
                    users = User.objects.all().order_by('f_name')
                elif sort == 'byDscName':
                    users = User.objects.all().order_by('-f_name')
                elif sort == 'byAscDate':
                    users = User.objects.all().order_by('up_date')
                elif sort == 'byDscDate':
                    users = User.objects.all().order_by('-up_date')
                else:
                    return HttpResponseRedirect('displayusers.html')
                return render(request, 'displayusers.html?msg="' + sort + '"', {'users': users})
            else:
                return HttpResponseRedirect('displayusers.html')
        else:
            return HttpResponseRedirect('displayusers.html')

    def showUserDetails(request):
        if 'admin' in request.session and request.session['admin'] is not None:
            uname=request.GET['user']
            users = User.objects.all()
            user = User.objects.get(uname=uname)
            return render(request, 'displayusers.html', {'users': users, 'userDetails': user})
        context = RequestContext(request)
        c = {}
        c.update(csrf(request))
        return render_to_response('adminlogin.html', c, context)