# Something in lines of http://stackoverflow.com/questions/348630/how-can-i-download-all-emails-with-attachments-from-gmail
# Make sure you have IMAP enabled in your gmail settings.
# Right now it won't download same file name twice even if their contents are different.


import email
import getpass, imaplib
import os

from LogToFile import get_latest_uid, write_latest_uid

detach_dir = '.'
if 'attachments' not in os.listdir(detach_dir):
    os.mkdir('attachments')


userName = 'dummy@xxx.com'
passwd = 'xxx'

mail_count = 0
saved_attachements_count = 0
# passwd = getpass.getpass('Enter your password: ')


imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
typ, accountDetails = imapSession.login(userName, passwd)

if typ != 'OK':
    print('Not able to sign in!')

imapSession.select()

typ, data = imapSession.uid('search', None, 'ALL')
# typ, data = imapSession.search(None, 'UNSEEN')


if typ != 'OK':
    print('Error searching Inbox.')


last_uid = get_latest_uid()

# Iterating over all emails
for msg_uid in data[0].split():
    if int(msg_uid) > last_uid:
        # fetch the email body (RFC822) for the given ID
        typ, messageParts = imapSession.uid('fetch', msg_uid, '(RFC822)')
        if typ != 'OK':
            print('Error fetching mail.')

        emailBody = messageParts[0][1]
        mail = email.message_from_bytes(emailBody)

        sender_address = email.utils.parseaddr(mail['From'])[1]
        real_name = email.utils.parseaddr(mail['From'])[0]
        print('Erkannter Name: ' + real_name + ' | Sender Adresse: ' + sender_address)
        # print(sender_address)

        if real_name == '':
            real_name = sender_address

        if real_name not in os.listdir(detach_dir + '/attachments/'):
            os.mkdir(detach_dir + '/attachments/' + real_name)

        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                # print part.as_string()
                continue
            if part.get('Content-Disposition') is None:
                # print part.as_string()
                continue
            fileName = part.get_filename()

            if bool(fileName):
                filePath = os.path.join(detach_dir, 'attachments', real_name, fileName)
                if not os.path.isfile(filePath):
                    print('Saved Attachment - ' + fileName)
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                    saved_attachements_count += 1

        mail_count += 1

write_latest_uid(msg_uid)

print()
print('Anzahl der betrachteten EMails: ' + str(mail_count))
print('Anzahl der gespeicherten Dokumente: ' + str(saved_attachements_count))
imapSession.close()
imapSession.logout()

