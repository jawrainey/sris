# SRIS - Self Reporting Intervention Service

The goal of this application is to act autonomously as an automated SMS service by communicating and administrate brief motivational interventions ([BMI](http://journals.lww.com/jtrauma/Fulltext/2005/09001/Brief_Motivational_Interventions__An_Introduction.8.aspx)) to [patients](https://github.com/jawrainey/atc) with addictions.

This was developed to test the scope of SMS as a means of administrating BMIs and interacting with patients, and was developed under the guidance of [Simon Moore](http://www.cardiff.ac.uk/people/view/39454-moore-simon), and [Roger Whitaker](http://www.cs.cf.ac.uk/contactsandpeople/staffpage.php?emailname=r.m.whitaker).

**Note:** this and the [associated data acquisition application](https://github.com/jawrainey/atc) were developed for exploratory and novel research purposes, and have been made open-source to assist future developers in tackling similar problems.

## Conversational structure

Brief interventions are administrated through pre-defined [client specified responses](https://github.com/jawrainey/sris/blob/master/sris/config/client.json). Specifically, making use of open-ended questions, reflective summaries, and empathy (emotions) as a means of achieving BMI techniques. The conversational flow is as follows:

1. An [initial question](https://github.com/jawrainey/sris/blob/master/sris/config/client.json#L2-L5) and/or [opening message on a pre-configured day/time](https://github.com/jawrainey/sris/blob/master/sris/config/client.json#L8-L9) are sent to begin the conversation.
2. Once a user responds, an [open-ended question](https://github.com/jawrainey/sris/blob/master/sris/config/client.json#L11-L18) (OEQ) is asked.
3. A patient reflects, and then responds without restrictions.
4. The patient's message is read (split by term frequency and then compared to the [ontology](https://github.com/jawrainey/sris/blob/master/sris/config/ontology.json)) to detect [general concepts](https://github.com/jawrainey/sris/blob/master/sris/config/ontology.json#L3) to categorize the context of the message. Once context is applied, an appropriate summary is [selected](https://github.com/jawrainey/sris/blob/master/sris/config/client.json#L20-L52) and sent back to the user.

**Note:** this conversation flow continues until a [threshold](https://github.com/jawrainey/sris/blob/master/sris/config/client.json#L7) of OEQs has been sent.

# Deployment

## Environment variables

### disable debugging

The [configuration variable](https://github.com/jawrainey/sris/blob/master/manage.py#L6) `ENV` must be set to `prod` to disable debugging and enable `postgresql` database access. This can be achieved in heroku as such:

    heroku config:set ENV=prod

### local time zone

Your local (or desired) time must be set to ensure messages are sent [as expected](https://github.com/jawrainey/sris/blob/master/sris/config/client.json#L3). This can be achieved by setting the time zone variable:

    heroku config:add TZ="Europe/London"

### database access

To enable `postgresql` access, the [client and service database](https://github.com/jawrainey/sris/blob/master/settings.py#L32-L33) environment variables must be set to the string of your `postgresql` of your database.

    // Obtain the name of the SRIS database
    heroku config | grep DATABASE_URL
    // Replace RESULT with above grep output 
    heroku config:set SERVICE_DATABASE_URL="RESULT"
    // Replace CLIENT_URL with your client; the ATC database string
    heroku config:set CLIENT_DATABASE_URL="CLIENT_URL"

### SMS service settings

I opted to use [Twilio](https://www.twilio.com/) for this service, which has [three properties](https://github.com/jawrainey/sris/blob/master/settings.py#L17-L19) that need to be set: `ACCOUNT_SID`, `AUTH_TOKEN`, `NUM`.

## Building locally

### Installing dependencies

I recommend creating a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) when developing:

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

**Note:** there may be difficulties when installing `psycopg2` on OSX. To resolve this, you should install it separately via brew, or remove it from `requirements.txt` as it's the engine for postgresql, which is not used for local development and testing.

### Shell access

For shell access to the `app` and `db` variables, pass the `shell` parameter to `manage.py`:

    python manage.py shell

This is useful for creating the database locally, and adding values to it, e.g. for testing:

    >>> db.create_all()
    >>> from sris import models
    >>> print len(db.session.query(models.User).all())

#### Running timed services

To run the [timed service](https://github.com/jawrainey/sris/blob/master/manage.py#L15-L27) (e.g. send daily message to begin conversation) pass the `timed_services` parameter to `manage.py`:

    python manage.py timed_services

## License

- Licensed under [MIT](https://github.com/jawrainey/sris/blob/master/LICENSE.txt).

## Contributing

If you have any suggestions then please open an [issue](https://github.com/jawrainey/sris/issues) or make a [pull request](https://github.com/jawrainey/sris/pulls).