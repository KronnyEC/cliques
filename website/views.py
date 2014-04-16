from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.db.models import Count
from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import ListView, CreateView, DetailView, \
    UpdateView
from website.models import Post, PostForm, CommentForm, Comment, UserProfile, \
    Category
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponse
from django.utils.importlib import import_module


def home(request):
    template_data = {}
    template_data['posts'] = Post.object.order_by('submitted')[:25]
    return render_to_response('homepage.html',
                              template_data,
                              context_instance=RequestContext(request))


def post(request, post_id):
    template_data = {}
    try:
        post = Post.object.get(id=post_id)
    except (Post.MultipleObjectsReturned, ObjectDoesNotExist):
        return HttpResponseNotFound("No post {}".format(post_id))
    return render_to_response('post.html',
                              template_data,
                              context_instance=RequestContext(request))


def warmup(request):
    """
    Provides default procedure for handling warmup requests on App
    Engine. Just add this view to your main urls.py.
    """
    for app in settings.INSTALLED_APPS:
        for name in ('urls', 'views', 'models'):
            try:
                import_module('%s.%s' % (app, name))
            except ImportError:
                pass
    content_type = 'text/plain; charset=%s' % settings.DEFAULT_CHARSET
    return HttpResponse("Warmup done.", content_type=content_type)


def user_redirect(request):
    return redirect('/users/{}'.format(request.user.username))


class PostsListView(ListView):
    model = Post
    template_name = 'website/post_list.html'

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        if self.queryset is not None:
            queryset = self.queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        elif self.model is not None:
            queryset = self.model._default_manager.all().select_related(*['user', 'category', 'comment_set'])
        else:
            raise ImproperlyConfigured("'%s' must define 'queryset' or 'model'"
                                       % self.__class__.__name__)
        queryset = queryset.annotate(comment_count=Count('comment'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PostsListView, self).get_context_data(**kwargs)
        context['form'] = PostForm
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'website/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['form'] = PostForm
        return context

    def get_queryset(self):
        category_name = self.request.GET.get('category')
        print "CATNAME", category_name
        category = Category.objects.get(name=category_name)
        qs = super(CategoryListView, self).get_queryset()
        qs = qs.filter(category=category.id)
        print "QUERY", qs
        return qs


class PostDetailView(DetailView):
    model = Post
    template_name = 'website/post.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm
        return context


class PostFormView(CreateView):
    model = Post
    fields = ['title', 'url', 'category']
    success_url = '/'
    # form_class = PostForm

    def form_valid(self, form):
        print "FORMVALID"
        user_model = get_user_model()
        form.instance.user = user_model.objects.get(id=self.request.user.id)
        self.object = form.save()
        return super(PostFormView, self).form_valid(form)


class CommentFormView(CreateView):
    model = Comment
    success_url = '/'
    fields = ['text']
    # template_name = 'website/post.html'

    def form_valid(self, form):
        user_model = get_user_model()
        form.instance.post = Post.objects.get(id=self.kwargs.get('pk'))
        form.instance.user = user_model.objects.get(id=self.request.user.id)
        #print form
        self.object = form.save()
        #print self.object
        self.success_url = "/post/{}/".format(self.kwargs.get('pk'))
        return super(CommentFormView, self).form_valid(form)
    # def get_initial(self):
    #     post = get_object_or_404(Post, id=s)
    #     print "post", post
    #     return {
    #         'post': post
    #     }


    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #     # form.send_email()
    #     print "form valid"
    #     return super(PostFormView, self).form_valid(form)


# def user_registered_callback(sender, user, request, **kwargs):
#     profile = UserProfile(user=user)
#     profile.is_human = bool(request.POST["is_human"])
#     profile.save()

# user_registered.connect(user_registered_callback)

class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'website/profile.html'


class ProfileEditView(UpdateView):
    template_name = 'website/profile.html'
    # form_class = ProfileUpdateForm
    model = UserProfile
    fields = ['email', 'email_settings']
    slug_field = 'username'
