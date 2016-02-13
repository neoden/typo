import os
import re
import uuid
import smtplib

from flask import render_template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.charset import Charset
from email.header import Header
from email.utils import formataddr, parseaddr
from email.encoders import encode_quopri


class Mail:
    def __init__(self):
        pass

    def init_app(self, app):
        self.default_sender = app.config.get('MAIL_DEFAULT_SENDER')
        self.mail_enabled = app.config.get('MAIL_ENABLED', True)
        self.mail_server = app.config.get('MAIL_SERVER', '127.0.0.1')
        self.mail_port = app.config.get('MAIL_PORT', 25)

    def _contact(self, address):
        if isinstance(address, tuple):
            return formataddr((Charset('utf-8').header_encode(address[0]), address[1]))
        else:
            return address

    def _contact_list(self, address_list):
        return ', '.join((self._contact(address) for address in address_list))

    def _address(self, contact):
        return contact[1] if isinstance(contact, tuple) else contact

    def _extract_statics(self, html):
        """
        Ищем в теле html картинки, и если src ссылается на static, выдираем ресурс в виде абсолютного
        пути к файлу, а тег img модифицируем, чтобы он ссылался на аттачмент
        Возвращаем модифицированный html и словарь с картинками вида:
        {
            'image0': <путь>,
            ...
        }
        """
        images = {}
        srcs_found = set()

        # теги img
        # весь тег кладётся в именованную группу img, src в группу src
        re_static_img = re.compile("(?P<img><img\s+[^>]*?src\s*=\s*['\"](?P<src>/static/[^'\"]*?)['\"][^>]*?>)")

        for m in re_static_img.finditer(html):
            src = m.groupdict()['src']
            if src not in srcs_found:
                srcs_found.add(src)
                cid = 'image_{}'.format(uuid.uuid4().hex)
                images[cid] = {
                    'orig_path': src,
                    'abs_path': os.path.join(current_app.root_path, src[1:]),
                }

        for cid, v in images.items():
            html = html.replace(v['orig_path'], 'cid:{}'.format(cid))

        return html, {k: v['abs_path'] for k, v in images.items()}        

    def _get_extension(self, path):
        s = path.rsplit('.', 1)
        if len(s) == 1:
            # no extension
            return ''
        else:
            return '.' + s[-1]

    def _attach_images(self, msgRoot, images):
        """
        Аттачит картинки к письму

        msgRoot - MIMEMultipart, куда присобачиваются вложения
        images - словарь вида: 
            {
                '<имя>': <путь>,
                ....
            }
        """
        for name, path in images.items():
            with open(path, 'rb') as f:
                msgImage = MIMEImage(f.read())
                msgImage.add_header('Content-ID', '<{}>'.format(name))
                msgImage.add_header('Content-Disposition', 'attachment; filename={}{}'.format(
                    str(name), self._get_extension(path)))
                msgRoot.attach(msgImage)

    def send(self, subject, recipients, sender=None, attach=None,
             html=None, text=None, template=None, **kwargs):
        """
        Отправка самосборного письма.
        Ссылки на картинке в статике превращаются в аттачменты. Текст правильно кодируется, чтобы
        избежать багов с переносом строки в Flask-Mail

        recipients - список
        attach - вложения, словарь имя-путь
        template - можно указать имя шаблона без расширения

        """

        sender = sender or self.default_sender

        if template:
            html, text = render_email(template, **kwargs)

        recipients_str = self._contact_list(recipients)

        charset = Charset(input_charset='utf-8')

        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = charset.header_encode(subject)
        msgRoot['From'] = self._contact(sender)
        msgRoot['To'] = recipients_str
        msgRoot.preamble = 'This is a multi-part message in MIME format.'
        msgRoot.set_charset('utf-8')

        msgAlternative = MIMEMultipart(_subtype='alternative')
        msgAlternative.set_charset("utf-8")
        msgRoot.attach(msgAlternative)

        msgText = MIMEText(_text=text, _subtype='plain', _charset='utf-8')
        msgAlternative.attach(msgText)

        html, images = self._extract_statics(html)
        self._attach_images(msgRoot, images)
        if attach:
            self._attach_images(msgRoot, attach)

        msgHtml = MIMEText(_text=html, _subtype='html', _charset='utf-8')
        msgAlternative.attach(msgHtml)

        if self.mail_enabled:
            with smtplib.SMTP(host=self.mail_server, port=self.mail_port) as smtp:
                smtp.sendmail(
                    self._address(sender),
                    [self._address(r) for r in recipients], 
                    msgRoot.as_string()
                )


    def bulk_send(self, subject, recipients, sender='info@landlord.ru', attach=None,
                  html_body=None, text_body=None, template=None, **kwargs):
        """
        Отправка письма нескольким адресатам. Каждый получит свой собственный экземпляр.

        recipients - список
        attach - вложения, словарь имя-путь
        """
        if current_app.config['MAIL_ENABLED']:
            for recipient in recipients:
                self.send(subject, [recipient], sender, attach,
                          html_body, text_body, template, **kwargs)

    def render_email(self, name, **kwargs):
        return (render_template(name + '.html', **kwargs),
                render_template(name + '.txt', **kwargs))
