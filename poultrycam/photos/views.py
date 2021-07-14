from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from ftp.connector import FtpConnector
from .models import Photo, MARKER_NEW, MARKER_GOOD, MARKER_BAD, MARKER_SKIP
from .forms import PhotoMarkersForm



# Create your views here.
class HomePageView(LoginRequiredMixin, FormView):
    template_name = 'photos/photo_form.html'
    form_class = PhotoMarkersForm
    login_url = 'users:login'

    def form_valid(self, form):
        photo = get_object_or_404(Photo, pk=form.cleaned_data['id'])
        if form.data.get('Mark_as_good', None):
            photo.marker = MARKER_GOOD
            photo.save()
        elif form.data.get('Mark_as_bad', None):
            photo.marker = MARKER_BAD
            photo.save()
        elif form.data.get('Skip', None):
            photo.marker = MARKER_SKIP
            photo.save()
        else:
            raise Exception(f'Invalide marker for photo')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('photos:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.update_photos_list()
        photo = Photo.objects.filter(marker=MARKER_NEW).first()
        context['photo'] = photo
        context['form'] = PhotoMarkersForm(initial={'id': photo.id, })
        context['photos_total'] = Photo.objects.all().count()
        context['photos_new'] = Photo.objects.filter(marker=MARKER_NEW).count()
        context['photos_marked_as_good'] = Photo.objects.filter(marker=MARKER_GOOD).count()
        context['photos_marked_as_bad'] = Photo.objects.filter(marker=MARKER_BAD).count()
        context['photos_skiped'] = Photo.objects.filter(marker=MARKER_SKIP).count()
        return context

    def update_photos_list(self):
        ftp = FtpConnector()
        ftp.update_photos_list('inbox')




