from django.core.paginator import Paginator


class ShortPaginator(Paginator):
    def page(self, page_number):
        self.current_page = super(ShortPaginator, self).page(page_number)
        return self.current_page

    def left_page_range(self):
        left_list = []
        if self.current_page.number > 5:
            left_list.append(1)
            left_list.append(None)
            left_list.append(self.current_page.number - 2)
            left_list.append(self.current_page.number - 1)

            return left_list
        else:
            return range(1, self.current_page.number)

    def right_page_range(self):
        left_list = []
        page_diff = self.num_pages - self.current_page.number
        if page_diff > 5:
            left_list.append(self.current_page.number + 1)
            left_list.append(self.current_page.number + 2)
            left_list.append(None)
            left_list.append(self.num_pages)

            return left_list
        else:
            return range(self.current_page.number + 1, self.num_pages + 1)
