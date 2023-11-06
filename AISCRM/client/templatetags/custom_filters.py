from django import template

register = template.Library()

@register.filter
def get_pagination_range(current_page, max_page_count):
    middle_value = max_page_count // 2
    total_pages = current_page.paginator.num_pages

    if current_page.number <= middle_value:
        start_page = 1
        end_page = min(total_pages, max_page_count)
    elif current_page.number > total_pages - middle_value:
        start_page = max(1, total_pages - max_page_count + 1)
        end_page = total_pages
    else:
        start_page = current_page.number - middle_value
        end_page = current_page.number + middle_value

    return range(start_page, end_page + 1)