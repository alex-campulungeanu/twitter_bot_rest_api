from flask import render_template
from flask import current_app
from flask_mail import Message

from app.constants import app_constants


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    current_app.logger.info(msg)
    # msg.send(msg)
    
def send_password_reset_email(user):
    token = user.get_forgot_password_token()
    send_email('[{0}] send reset email'.format(app_constants.reset_mail_subject_app),
            #    sender=app.config['ADMINS'][0],
               sender=current_app.config['MAIL_SENDER'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, p_token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, p_token=token)
               )
