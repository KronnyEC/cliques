from mimetypes import guess_type
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import ListView, FormView, CreateView, DetailView, \
    UpdateView
from website.models import Post, PostForm, CommentForm, Comment, UserProfile, \
    ProfileUpdateForm
from django.conf import settings
# from registration.signals import user_registered
from django.contrib.auth import get_user_model


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


class PostsListView(ListView):
    model = Post
    template_name = 'website/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(PostsListView, self).get_context_data(**kwargs)
        context['form'] = PostForm
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'website/post.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm
        return context


class PostFormView(CreateView):
    model = Post
    fields = ['title', 'url',]
    success_url = '/'

    def form_valid(self, form):
        user_model = get_user_model()
        form.instance.user = user_model.objects.get(id=self.request.user.id)
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
