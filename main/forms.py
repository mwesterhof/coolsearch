from django import forms
from searcher.register import modelindex


class SearchForm(forms.Form):
    query = forms.CharField()

    def do_search(self):
        query = self.cleaned_data['query']
        results = modelindex.search(query)
        return results
