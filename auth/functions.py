"""Auth funtions."""
import uuid
from django.utils import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from .models import AccountVerification, AppUser
from .emails import send_email


def send_verification(request, email, more=None):
    """Method to send verification."""
    try:
        print 'account_created'
        uid = uuid.uuid4()
        suid = str(uid)
        save_verification(email, uid)
        # host = 'portal.marineinsurance.co.ke'
        host = Site.objects.get_current()
        domain = 'https://%s/account/' % (host)
        url = '%s?uid=%s&email=%s' % (domain, suid, email)
        ebody = ''
        if more:
            ebody += more
        ebody += '<p>To complete the registration click this link '
        ebody += '<a href="%s">%s</a></p> ' % (url, url)
        ebody += 'Marine Insurance.\n'
        msg = 'Hi!\n To complete the registration copy and paste the link '
        msg += '%s in your browser\n\n' % (url)
        msg += 'Marine Insurance.\n'
        send_email(email, msg, ebody, settings)
    except Exception, e:
        print 'error sending email - %s' % (str(e))
        pass
    else:
        pass


def save_verification(email, uid):
    """Method to send verification."""
    try:
        health, created = AccountVerification.objects.update_or_create(
            email=email,
            defaults={'email': email, 'verified': False,
                      'verification_code': uid},)
    except Exception, e:
        print 'error saving verification - %s' % (str(e))
        pass
    else:
        pass


def perform_verification(email, uid):
    """Method to send verification."""
    try:
        result = False
        todate = timezone.now()
        acc_detail = get_object_or_404(
            AccountVerification, email=email, verification_code=uid)
        if acc_detail:
            result = True
            user_detail = get_object_or_404(AppUser, email=email)
            user_detail.email_verified = True
            user_detail.save(
                update_fields=["email_verified"])
            # Also update verification details
            acc_detail.verified = True
            acc_detail.verified_at = todate
            acc_detail.save(
                update_fields=["verified", "verified_at"])
    except Exception, e:
        print 'error checking verification - %s' % (str(e))
        return False
    else:
        return result


def create_account(email, client_type_id, password):
    """Method to create account."""
    try:
        result = False
        user = AppUser.objects.create_user(email=email,
                                           person_type=client_type_id,
                                           password=password)
        if user:
            result = user
    except Exception, e:
        print 'error creating account - %s' % (str(e))
        return False
    else:
        return result
