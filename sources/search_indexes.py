import datetime
from haystack import indexes
from .models import Person


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
	## EXAMPLES
    # text = indexes.CharField(document=True, use_template=True)
    # author = indexes.CharField(model_attr='user')
    updated = indexes.DateTimeField(model_attr='updated')
    ## title, organization, type_of_expert, language, timezone, city, state, country, notes,
    text = indexes.CharField(document=True, use_template=True)


    def get_model(self):
        return Person

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(updated__lte=datetime.datetime.now())