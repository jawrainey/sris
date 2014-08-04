from sris import db, models
from flask import request, Blueprint, make_response
from manager import Manager

bp = Blueprint('service', __name__)


@bp.route("/sms/", methods=['GET', 'POST'])
def sms():
    """
    Responds to an SMS message sent to the service account if patient known.
    """
    known_patients = [item.mobile for item in
                      db.session.query(models.Patient.mobile).all()]
    number = request.values.get('From')
    message = request.values.get('Body')

    if not message:
        print 'No message was sent by the patient...'
        return ''

    if number in known_patients:
        print "Attempting to send SMS response to %s" % (number)
        return make_response(Manager().respond(
            {'message': message, 'number': number}))
    else:
        print 'Logging that an unknown patient has sent the service an SMS.' + \
            'Their mobile number and message was: %s, %s' % (number, message)
        return ''
