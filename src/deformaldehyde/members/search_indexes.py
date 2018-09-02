from haystack import indexes
from members.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        # import pdb;pdb.set_trace()
        return self.get_model().objects.all()
