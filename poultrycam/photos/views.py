from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Photo, MARKER_NEW, MARKER_GOOD, MARKER_BAD, MARKER_SKIP
from .forms import PhotoMarkersForm


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
        photo = Photo.objects.filter(marker=MARKER_NEW).first()
        if photo:
            context['photo'] = photo
            context['form'] = PhotoMarkersForm(initial={'id': photo.id, })
        context['stat'] = get_photos_statistic()
        return context



class PhotoListView(LoginRequiredMixin, ListView):
    model = Photo
    paginate_by = 12
    template_name = 'photos/photos_list.html'
    login_url = 'users:login'
    mark = None

    def get_queryset(self):
        return Photo.objects.filter(marker=self.mark).order_by('id')

    def get_context_data(self, **kwargs):
        context = super(PhotoListView, self).get_context_data(**kwargs)
        context['stat'] = get_photos_statistic()
        context['title'] = mark_to_text(self.mark)
        return context




def get_photos_statistic():
    statistic = {}
    statistic['photos_total'] = Photo.objects.all().count()
    statistic['photos_new'] = Photo.objects.filter(marker=MARKER_NEW).count()
    statistic['photos_marked_as_good'] = Photo.objects.filter(marker=MARKER_GOOD).count()
    statistic['photos_marked_as_bad'] = Photo.objects.filter(marker=MARKER_BAD).count()
    statistic['photos_skiped'] = Photo.objects.filter(marker=MARKER_SKIP).count()
    return statistic


def mark_to_text(mark):
    if mark == MARKER_NEW:
        return 'Новые фотографии'
    elif mark == MARKER_GOOD:
        return 'Хорошие фотографии'
    if mark == MARKER_BAD:
        return 'Плохие фотографии'
    elif mark == MARKER_SKIP:
        return 'Пропущенные фотографии'

