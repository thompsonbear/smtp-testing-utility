import smtplib

#Attempts to connect the the SMTP server - prints an error on failure
def test_conn(sender_address, sender_password, smtp_server, smtp_server_port, start_tls_enabled):
    print("\nAttempting connection with the following settings:\n")
    print_smtp_settings(sender_address, sender_password, smtp_server, smtp_server_port, start_tls_enabled)
    with smtplib.SMTP(smtp_server, smtp_server_port) as smtp:
        smtp.ehlo()
        if(start_tls_enabled):
            smtp.starttls()
            smtp.ehlo()
        try:
            smtp.login(sender_address, sender_password)
        except (smtplib.SMTPAuthenticationError, smtplib.SMTPNotSupportedError, smtplib.SMTPHeloError, 
        smtplib.SMTPConnectError, smtplib.SMTPDataError, smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused, 
        smtplib.SMTPResponseException, smtplib.SMTPServerDisconnected, smtplib.SMTPException) as e:
            print("Error connecting to server:\n" + str(e))
            return
    print("Connection was successful!\n")

#Attempts to connect the the SMTP server - prints an error on failure - sends an email on success
def send_test_email(sender_address, sender_password, smtp_server, smtp_server_port, start_tls_enabled, email_subject, email_recipient):
    print("\nAttempting to send email with the following settings:\n")
    print_smtp_settings(sender_address, sender_password, smtp_server, smtp_server_port, start_tls_enabled, email_subject, email_recipient)
    with smtplib.SMTP(smtp_server, smtp_server_port) as smtp:
        smtp.ehlo()
        if(start_tls_enabled):
            smtp.starttls()
            smtp.ehlo()
        try:
            smtp.login(sender_address, sender_password)
        except (smtplib.SMTPAuthenticationError, smtplib.SMTPNotSupportedError, smtplib.SMTPHeloError, 
        smtplib.SMTPConnectError, smtplib.SMTPDataError, smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused, 
        smtplib.SMTPResponseException, smtplib.SMTPServerDisconnected, smtplib.SMTPException) as e:
            print("Error sending test email:\n" + str(e))
            return
        message = f'Subject: {email_subject}\n\nTest email from SMTP Testing Utility'
        smtp.sendmail(sender_address, email_recipient, message)
    print("Email was sent successfully!\n")

def print_smtp_settings(sender_address, sender_password, smtp_server, smtp_server_port, start_tls_enabled, email_subject = False, email_recipient = False):
    print(f'Sender Address: {sender_address}')
    print(f'Sender Password: {sender_password}')
    print(f'SMTP Server: {smtp_server}')
    print(f'SMTP Server Port: {smtp_server_port}')
    print(f'Start TLS Enabled: {start_tls_enabled}\n')
    if(email_subject):
        print(f'Email Subject: {email_subject}')
    if(email_recipient):
        print(f'Email Recipients: {email_recipient}\n')


sender_address = False
sender_password = False
smtp_server = False
smtp_server_port = False

test_again = True
print("Python CLI SMTP Testing Utility\n")
while test_again:

    answer = input(f'Enter sender address{f" (Blank for {sender_address})" if sender_address else ""}: ')
    if (answer != "" or sender_address == False):
        sender_address = answer

    answer = input(f'Enter sender password{f" (Blank for {sender_password})" if sender_password else ""}: ')
    if (answer != "" or sender_password == False):
        sender_password = answer

    answer = input(f'Enter SMTP server{f" (Blank for {smtp_server})" if smtp_server else ""}: ')
    if (answer != "" or smtp_server == False):
        smtp_server = answer

    answer = input(f'Enter SMTP server port{f" (Blank for {smtp_server_port})" if smtp_server_port else ""}: ')
    if (answer != "" or smtp_server_port == False):
        smtp_server_port = answer

    answer = input("Enable Start TLS? (Y)/N: ")
    if (answer == "" or answer.upper() == "Y"):
        start_tls_enabled = True
    else:
        start_tls_enabled = False

    answer = "0"
    while answer != "test" and answer != "send":
        answer = input("Would you like to only test the SMTP connection (test) or also send a test email (send)?: ")
        if answer.lower() == "test":
            test_conn(sender_address, sender_password, smtp_server, smtp_server_port, start_tls_enabled)
        elif answer.lower() == "send":
            email_subject = input("What would you like the email subject to be?: ")
            email_recipient = input("Enter the recipient address: ")
            send_test_email(sender_address, sender_password, smtp_server, smtp_server_port, start_tls_enabled, email_subject, email_recipient)
        else:
            print("Invalid entry.")

    answer = input("Would you like to do another test? (Y)/N: ")
    if (answer == "" or answer.upper() == "Y"):
        test_again = True
    else:
        test_again = False
        print("Exiting..")