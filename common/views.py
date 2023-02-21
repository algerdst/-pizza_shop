class ContextMixin:
    title = None
    categories = None
    queryset = None

    def get_context_data(self, **kwargs):
        context = super(ContextMixin, self).get_context_data(**kwargs)
        context['categories'] = self.categories
        return context

    def get_queryset(self):
        queryset = self.queryset
        return queryset
