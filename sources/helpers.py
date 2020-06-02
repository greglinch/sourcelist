from PIL import Image, ImageDraw, ImageFont

from sourcelist.settings import MEDIA_ROOT


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


def generate_image_from_text(source_id, text_content, field_name):
    # 250 for phone numbers is probably enough
    image = Image.new('RGB', (500, 25), color=(255,255,255))
    font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 21)
    drawn_image = ImageDraw.Draw(image)
    drawn_image.text((0,0), text_content, font=font, fill=(0,0,0))
    image_location = f'{MEDIA_ROOT}images/{field_name}/{source_id}.png'
    image.save(image_location)

    return image_location
