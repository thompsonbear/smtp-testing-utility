import smtplib
import socket
import urllib.request

def test_smtp(sender_address, sender_password, smtp_server, smtp_server_port, start_tls_enabled, email_subject=False, email_recipient=False):
    # Print all provided settings
    print("\nConfigured Settings:\n")
    print(f'Sender Address: {sender_address}')
    print(f'Sender Password: {sender_password}')
    print(f'SMTP Server: {smtp_server}')
    print(f'SMTP Server Port: {smtp_server_port}')
    print(f'Start TLS Enabled: {start_tls_enabled}\n')
    if(email_subject):
        print(f'Email Subject: {email_subject}')
    if(email_recipient):
        print(f'Email Recipients: {email_recipient}\n')

    try:
        print("Testing server connection...")
        # Establish a connection/session with the server
        with smtplib.SMTP(smtp_server, smtp_server_port) as smtp:
            # Identify self to the esmtp server
            smtp.ehlo()
            # If start_tls_enabled is true, add starttls to the session and re-identify to the server
            if(start_tls_enabled):
                smtp.starttls()
                smtp.ehlo()
            # Login to the smtp server 
            smtp.login(sender_address, sender_password)
            print("Connection was successful!\n")
            # If email subject and recipient are also provided, attempt to send a test email
            if(email_subject and email_recipient):
                print("Sending test email...")
                # Formats and sends email subject and body
                message = f'Subject: {email_subject}\n\nTest email from SMTP Testing Utility\n\nSent from IP: {client_public_ip()}'
                smtp.sendmail(sender_address, email_recipient, message)
                print("Email was sent successfully!\n")
    # Catch all exceptions related to smtplib
    except smtplib.SMTPException as e:
        print("[SMTP Error] Message:\n" + str(e))
        return
    # Catch socket errors, normally timeouts for bad ports
    except socket.error as e:
        print("[Connection Error] Message:\n" + str(e))
        return
# Gets and returns client public IP from ident.me
def client_public_ip():
    return urllib.request.urlopen('https://ident.me').read().decode('utf8')

if __name__== "__main__" :
    # Set initial values to false so alternate text is not printed in user input requests
    sender_address = False
    sender_password = False
    smtp_server = False
    smtp_server_port = False

    test_again = True
    print("Python CLI SMTP Testing Utility\n")
    while test_again:
        # Get test case information from user
        # If this is not the first run, data currently stored will be used
        user_input = input(f'Enter sender address{f" (Blank for {sender_address})" if sender_address else ""}: ')
        if (user_input != "" or sender_address == False):
            sender_address = user_input
        user_input = input(f'Enter sender password{f" (Blank for {sender_password})" if sender_password else ""}: ')
        if (user_input != "" or sender_password == False):
            sender_password = user_input
        user_input = input(f'Enter SMTP server{f" (Blank for {smtp_server})" if smtp_server else ""}: ')
        if (user_input != "" or smtp_server == False):
            smtp_server = user_input
        user_input = input(f'Enter SMTP server port{f" (Blank for {smtp_server_port})" if smtp_server_port else ""}: ')
        if (user_input != "" or smtp_server_port == False):
            smtp_server_port = user_input
        user_input = input("Enable Start TLS? (Y)/N: ")
        if (user_input == "" or user_input.upper() == "Y"):
            start_tls_enabled = True
        else:
            start_tls_enabled = False
        user_input = "" # Set input to none to ensure following while loop runs as expected
        # Calls function without email subject and recipient if test is entered or 
        # gets subject and recipient before passing all parameters to the function which will then send an email also
        while user_input != "test" and user_input != "send":
            user_input = input("Would you like to only test the SMTP connection (test) or also send a test email (send)?: ")
            if user_input.lower() == "test":
                test_smtp(sender_address, sender_password, smtp_server, smtp_server_port, start_tls_enabled)
            elif user_input.lower() == "send":
                email_subject = input("What would you like the email subject to be?: ")
                email_recipient = input("Enter the recipient address: ")
                test_smtp(sender_address, sender_password, smtp_server, smtp_server_port, start_tls_enabled, email_subject, email_recipient)
            else:
                print("Invalid entry.")
        # Ask user if they would like to do another test or exit
        user_input = input("\nWould you like to do another test? (Y)/N: ")
        if (user_input == "" or user_input.upper() == "Y"):
            test_again = True
        else:
            test_again = False
            print("Exiting...")