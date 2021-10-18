from django.views.generic import DetailView, FormView

from .forms import SearchForm
from .models import Job, Person


class HomeView(FormView):
    template_name = 'main/home.html'
    form_class = SearchForm

    def form_valid(self, form):
        results = form.do_search()

        return self.render_to_response(
            self.get_context_data(
                results=results
                )
            )


class JobDetail(DetailView):
    model = Job


class PersonDetail(DetailView):
    model = Person
