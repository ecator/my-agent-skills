# /// script
# dependencies = [
#   "python-dotenv",
# ]
# ///

import os
import argparse
import smtplib
import mimetypes
from email.message import EmailMessage
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)


def send_mail(
    sender_email, to_email, subject, body_text=None, body_html=None, attachments=None
):
    """
    Sends an email using the provided parameters and SMTP settings from environment variables.
    """
    # Connection info from environment variables
    smtp_server = os.getenv("SENDMAIL_SMTP_SERVER")
    smtp_port = os.getenv("SENDMAIL_SMTP_PORT", "465")
    smtp_user = os.getenv("SENDMAIL_SMTP_USER")
    smtp_password = os.getenv("SENDMAIL_SMTP_PASSWORD")

    if not all([smtp_server, smtp_user, smtp_password]):
        print(
            "Error: SENDMAIL_SMTP_SERVER, SENDMAIL_SMTP_USER, and SENDMAIL_SMTP_PASSWORD must be set as environment variables."
        )
        sys.exit(1)

    # Create EmailMessage object (modern Python email handling)
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    # Define content logic: text vs html
    if body_html:
        # HTML content
        msg.set_content(body_html, subtype="html")
    elif body_text:
        # Plain text content
        msg.set_content(body_text)
    else:
        print("Error: Email body content is missing.")
        sys.exit(1)

    # Add attachments
    if attachments:
        for file_path in attachments:
            if not os.path.isfile(file_path):
                print(f"Warning: Attachment file not found: {file_path}")
                continue

            # Guess mime type
            ctype, encoding = mimetypes.guess_type(file_path)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"
            maintype, subtype = ctype.split("/", 1)

            with open(file_path, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype=maintype,
                    subtype=subtype,
                    filename=os.path.basename(file_path),
                )

    # Send via SMTP
    # print(f"Connecting to {smtp_server}:{smtp_port}...")
    try:
        # Use implicit SSL if port is 465 (usually)
        # However, testing showed port 465 on this server is NOT implicit SSL
        # So we'll use SMTP and then STARTTLS
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            # server.set_debuglevel(1) # Uncomment for detailed logs
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            print(f"Email sent to {to_email} successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send an email with SSL support and attachments."
    )
    parser.add_argument("--sender", required=True, help="Sender email address")
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--subject", required=True, help="Subject of the email")
    parser.add_argument(
        "--bodyfile",
        required=True,
        help="Path to a .md, .txt or .html file for email body",
    )
    parser.add_argument(
        "--attach", nargs="*", help="Paths to files to attach (multiple allowed)"
    )

    args = parser.parse_args()

    # Determine body content and type from file extension
    body_text = None
    body_html = None

    if not os.path.isfile(args.bodyfile):
        print(f"Error: Body file not found: {args.bodyfile}")
        sys.exit(1)

    ext = os.path.splitext(args.bodyfile)[1].lower()
    try:
        with open(args.bodyfile, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading body file: {e}")
        sys.exit(1)

    if ext == ".txt" or ext == ".md":
        body_text = content
    elif ext == ".html":
        body_html = content
    else:
        print("Error: Body file extension must be .txt or .html")
        sys.exit(1)

    send_mail(
        sender_email=args.sender,
        to_email=args.to,
        subject=args.subject,
        body_text=body_text,
        body_html=body_html,
        attachments=args.attach,
    )
