search_customizations = {
    ## The name of the variable to contain the list of results (default 'search_results')
    # 'context_object_name': '',
    ## The list of models to exclude from search results (default empty list)
    # 'exclude': (),
    ## The page to redirect to if the user enters an empty search term (default None)
    # 'empty_query_redirect': '',
    ## A dictionary of values to add to the template context. By default, this is an empty dictionary. If a value in the dictionary is callable, the view will call it just before rendering the template.
    # 'extra_context': {},
    ## The list of models to search from (default all)
    # 'models': ('Person'),
    ## An integer specifying how many objects should be displayed per page (default None)
    # 'paginate_by': '',
    ## An integer specifying the page to display, or 'last'. If blank, then the GET parameter 'page' will be used (default None)
    # 'page': ,
    ## The GET parameter to use for the search term (default 'q').
    # 'query_param': '',
    ## The name of the template used to render the search results (default 'watson/search_results.html')
    'template_name': 'results.html',
}
