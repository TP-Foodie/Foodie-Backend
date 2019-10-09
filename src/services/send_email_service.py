from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_token(email, token):
    send_grid_api_client = SendGridAPIClient()
    _mail = Mail(
        from_email="foodie@norepy.com",
        to_emails=email,
        subject="Reseteo de contraseña",
        plain_text_content=f'Tu token de recuperacion de contraseña es {token}'
    )
    send_grid_api_client.client.mail.send.post(request_body=_mail.get())
