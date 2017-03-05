import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



class gmail:
    def __init__(self, address, passwd):
        self.address = address
        self.passwd = passwd

    def send_mail_from_file(self, toaddr, subject, path_to_file):
        body = open(path_to_file, "r")
        lengte = len(path_to_file)
        html = False
        if path_to_file[lengte - 4:lengte] == "html":
            html = True
        self.send_mail(toaddr, subject, body.read(), html)
        body.close()

    def send_mail(self, toaddr, subject, body, body_is_html=False):
        fromaddr = self.address

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject

        if body_is_html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, self.passwd)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

    def send_mail_with_attachement(self, toaddr, subject, filename, path_to_file, body, body_is_html=False):

        fromaddr = self.address

        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject

        if body_is_html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))

        attachment = open(path_to_file, "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, self.passwd)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
