import pytz
import datetime


MONTHS = {
    1: 'января', 
    2: 'февраля', 
    3: 'марта', 
    4: 'апреля', 
    5: 'мая', 
    6: 'июня', 
    7: 'июля', 
    8: 'августа', 
    9: 'сентября', 
    10: 'октября', 
    11: 'ноября', 
    12: 'декабря'
}


def now():
    return pytz.utc.localize(datetime.datetime.utcnow())


def register_jinja_filters(app):
    @app.template_filter('datetime')
    def datetime_(x):
        return x.strftime('%d.%m.%Y %H:%M')

    @app.template_filter('longdatetime')
    def longdatetime(x):
        return x.strftime('%d {} %Y в %H:%M'.format(MONTHS[x.month]))
