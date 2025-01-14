import boto3
from botocore.exceptions import ClientError
import os

class EmailService:
    def __init__(self):
        self.ses_client = boto3.client('ses',
            region_name=os.getenv('AWS_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        self.sender_email = os.getenv('SENDER_EMAIL', 'noreply@yourdomain.com')

    async def send_password_reset_email(self, recipient_email: str, reset_url: str):
        """Send password reset email using AWS SES."""
        try:
            subject = "Password Reset Request"
            html_body = f"""
            <html>
                <body>
                    <h2>Password Reset Request</h2>
                    <p>You have requested to reset your password. Click the link below to proceed:</p>
                    <p><a href="{reset_url}">Reset Password</a></p>
                    <p>This link will expire in 1 hour.</p>
                    <p>If you did not request this password reset, please ignore this email.</p>
                </body>
            </html>
            """
            text_body = f"""
            Password Reset Request
            
            You have requested to reset your password. Click the link below to proceed:
            {reset_url}
            
            This link will expire in 1 hour.
            
            If you did not request this password reset, please ignore this email.
            """

            response = self.ses_client.send_email(
                Source=self.sender_email,
                Destination={
                    'ToAddresses': [recipient_email]
                },
                Message={
                    'Subject': {
                        'Data': subject
                    },
                    'Body': {
                        'Text': {
                            'Data': text_body
                        },
                        'Html': {
                            'Data': html_body
                        }
                    }
                }
            )
            return response
        except ClientError as e:
            print(f"Error sending email: {str(e)}")
            raise e 