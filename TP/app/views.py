from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from api.service import Statistics
from app.models import Item


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        context = {
            'most_expensive': Statistics.most_expensive_item()[0]['name'],
            'most_pops': Statistics.most_popular(),
        }
        # html = template.render(context)
        pdf = render_to_pdf('table.html', context)
        return HttpResponse(pdf, 'table.html', content_type='application/pdf')
