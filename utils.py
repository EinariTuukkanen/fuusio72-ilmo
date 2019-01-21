# ======================================
# >>> IMPORTS
# ======================================

# Python
from time import time
import configparser

# Third-party
from string import Template

from flask_mail import Message


# ======================================
# >>> FUNCTIONS
# ======================================

def load_config(flask_app, mongo_db, config_filename):
    config = configparser.SafeConfigParser()
    config.optionxform = str
    config.read(config_filename)
    settings = dict()

    # Update Flask email configs
    flask_app.config.update(**dict(config.items('FlaskEmail')))

    for section in config.sections():
        settings[section] = dict(config.items(section))

    existing_config = mongo_db.config.find_one()
    if existing_config is None:
        settings['ReferenceNumber'] = settings['Billing']['InitialReference']
        mongo_db.config.save(settings)
    else:
        settings['ReferenceNumber'] = existing_config.get('ReferenceNumber')
        mongo_db.config.update(
            {'_id': existing_config.get('_id')},
            settings,
            upsert=True
        )

    return settings


def send_billing_mail(flask_mail, settings, user):
    email_templates = settings.get('EmailTemplates')
    billing = settings.get('Billing')
    max_users = int(settings['App']['MaxUsers'])

    # Status price
    if user.get('status') == u'student':
        bill_sum = int(billing.get('StudentPrice'))
    # elif user == u'supporter':
        # sum = int(billing.get('SupporterPrice'))
    else:
        bill_sum = int(billing.get('DefaultPrice'))

    # Sillis price
    if user.get('sillis') == 'true':
        bill_sum += int(billing.get('SillisPrice'))

    # History manuscript order price
    # if user.get('historyOrder') == 'true':
        # sum += int(billing.get('HistoryManuscriptPrice'))

    # History manuscript post price
    # if user.get('historyDeliveryMethod') == 'deliverPost':
        # sum += int(billing.get('PostDeliveryPrice'))

    # timestamp = int(time())

    # if (timestamp >= 1485770400
    #         and user.get('status') in ['student', 'notStudent']
    #         and user.get('guildStatus') == 'currentMember'):
    #     letter = Template(email_templates.get('Bill'))
    # else:
    #     letter = Template(email_templates.get('ThankYouLetter'))

    if int(user.get('index')) >= max_users:
        letter = Template(email_templates.get('QueueLetter'))
    elif user.get('status') in ['student', 'notStudent']:
        letter = Template(email_templates.get('Bill'))
    else:
        letter = Template(email_templates.get('ThankYouLetter'))

    # Format template
    email_templates.update({'sum': bill_sum})
    email_templates.update(user)
    email_templates.update({'br': '\n'})
    email_body = letter.safe_substitute(email_templates)

    print('Sending mail: {name} {email}'.format(
        name=user.get('name'),
        email=user.get('email')
    ))

    sent_successfully = send_flask_mail(
        flask_mail,
        email_templates.get('MailHeader'),
        email_templates.get('MailSender'),
        user.get('email'),
        email_body
    )

    # return False
    return sent_successfully


def send_flask_mail(flask_mail, subject, from_email, to_email, body):
    msg = Message(
        subject,
        sender=from_email,
        recipients=[to_email]
    )
    msg.body = body
    try:
        flask_mail.send(msg)
        return True
    except Exception as e:
        print('[ERROR] Failed to send email, ' + str(e))
        return False


def get_reference_number(mongo_db):
    return checksum(get_main_part(mongo_db))


def checksum(ref):
    r = str(ref)
    sum = 0
    m = [7, 3, 1]
    for i, s in enumerate(reversed(r)):
        sum += int(s) * m[i % 3]
    return r + str((10 - (sum % 10)) % 10)


def get_main_part(mongo_db):
    settings = mongo_db.config.find_one({'ReferenceNumber': {'$exists': 1}})
    if not settings:
        print('[ERROR] Could not find reference number, random generating...')
        return int(time())
    reference_number = int(settings.get('ReferenceNumber'))
    mongo_db.config.update(
        {'ReferenceNumber': {'$exists': 1}},
        {'$set': {'ReferenceNumber': str(reference_number + 1)}}
    )
    return reference_number

"""def reference_counter():
    reference_number = db.config.find_one({'referenceCounter':{'$exists': 1}})
    db.config.update({'_id': reference_number.get('_id')},
    {'referenceCounter': int(reference_number.get('referenceCounter')) +1})
    return int(reference_number.get('referenceCounter')) +1

if not db.config.find_one({'referenceCounter': {'$exists': 1}}):
    db.config.update(
        {'referenceCounter': {'$exists': 1}},
        {'referenceCounter': db.config.find_one({}, {'Billing': 1, '_id': 0}).
        get('Billing').get('InitialReference')}, upsert=True)"""
