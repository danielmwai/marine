"""Process custom base."""
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from .models import RegSites


def base_template(request):
    """Get site id."""
    site = Site.objects.get_current()
    sid = site.pk
    cods = get_site_details(sid)
    coid, cotype = 0, 0
    if cods:
        coid = cods.company_id
        cotype = cods.company_type
    tmpl = "base%s.html" % str(sid)
    vals = {'BASE_TEMPLATE': tmpl, 'SITE_ID': sid,
            'SITE_IDT': str(sid), 'CO_ID': coid, 'CO_TYPE': cotype}
    return vals


def get_site_details(sid):
    """Method to get company id."""
    try:
        company = get_object_or_404(RegSites, site_id=sid)
    except Exception:
        return None
    else:
        return company
