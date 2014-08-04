from sris import db, models
from flask import request, Blueprint
from manager import Manager

bp = Blueprint('service', __name__)


@bp.route("/sms/", methods=['POST'])
def sms():
    """
    Responds to an SMS message sent to the service account if patient known.
    """
    known_patients = [item.mobile for item in
                      db.session.query(models.Patient.mobile).all()]
    number = request.values.get('From').replace('+', '')
    message = request.values.get('Body')

    if number in known_patients:
        print "Attempting to send SMS response to %s" % (number)
        return Manager().respond({'message': message, 'number': number})
    else:
        print 'Logging that an unknown patient has sent the service an SMS.' + \
            'Their mobile number and message was: %s, %s' % (number, message)
        return ''
