import imaplib
import email
import traceback

username = "your_mail_address"
password = "your_password"
imap_host = "imap.gmail.com"
# filePath = '/home/followingjude/mysite/log.txt'
filePath = '../log.txt'


try:
    # Connect to host using SSL
    imap = imaplib.IMAP4_SSL(imap_host)
    # login to server
    imap.login(username, password)

    # Select all inbox messages
    imap.select('inbox')
    tmp, messages = imap.search(None, 'ALL')
    id_list = messages[0].split()

    # Open all messages
    for i in id_list:
        data = imap.fetch(i, '(RFC822)')
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1], 'utf-8'))
                email_subject = msg['subject']
                email_from = msg['from']
                # Check if mail is send by scrapper, and store data in log file
                if email_subject == "Data" and email_from == username:
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            text = part.get_payload()
                            with open(filePath, 'a') as file:
                                file.write(text)

    # Delete all messages
    for obj in id_list:
        imap.store(obj, "+FLAGS", "\\Deleted")
    imap.expunge()

    # Close connection
    imap.close()
    imap.logout()

except Exception as e:
    traceback.print_exc()
    print(str(e))
