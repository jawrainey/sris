from sris import app, db, models
from flask import request
from manager import Manager


@app.route("/sms/", methods=['GET', 'POST'])
def sms():
    """
    Responds to an SMS message sent to the service account if patient known.
    """
    known_patients = [item.mobile for item in
                      db.session.query(models.Patient.mobile).all()]
    number = request.values.get('From')
    message = request.values.get('Body')
    if number in known_patients:
        print "Sending SMS response to %s" % (number)
        return Manager().respond({'message': message, 'number': number})
    else:
        print 'Logging that an unknown patient has sent the service an SMS.' + \
            'Their mobile number and message was: %s, %s' % (number, message)
        return ''
