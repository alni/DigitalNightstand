# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import calendar
import inspect
import sys


def get_locale(name):
    '''Returns an appropriate :class:`Locale <locale.Locale>` corresponding
    to an inpute locale name.

    :param name: the name of the locale.

    '''

    locale_cls = _locales.get(name.lower())

    if locale_cls is None:
        raise ValueError('Unsupported locale \'{0}\''.format(name))

    return locale_cls()


# base locale type.

class Locale(object):
    ''' Represents locale-specific data and functionality. '''

    names = []

    alarm = {
        'next': '',
        'none': ''
    }

    def __init__(self):

        self._month_name_to_ordinal = None

    def get_alarm(self, alarm_time):
        alarm = self.alarm
        if alarm_time is not None:
            return alarm['next'].format(alarm_time)
        else:
            return alarm['next'].format(alarm['none'])


# base locale type implementations.

class EnglishLocale(Locale):

    names = ['en', 'en_us', 'en_gb', 'en_au', 'en_be', 'en_jp', 'en_za']

    alarm = {
        'next': 'Next alarm {0}',
        'none': '(no alarms set)'
    }


class ItalianLocale(Locale):
    names = ['it', 'it_it']


class SpanishLocale(Locale):
    names = ['es', 'es_es']


class FrenchLocale(Locale):
    names = ['fr', 'fr_fr']


class GreekLocale(Locale):

    names = ['el', 'el_gr']

class JapaneseLocale(Locale):

    names = ['ja', 'ja_jp']


class SwedishLocale(Locale):

    names = ['sv', 'sv_se']


class FinnishLocale(Locale):

    names = ['fi', 'fi_fi']

    # The finnish grammar is very complex, and its hard to convert
    # 1-to-1 to something like English.


class ChineseCNLocale(Locale):

    names = ['zh', 'zh_cn']


class ChineseTWLocale(Locale):

    names = ['zh_tw']


class KoreanLocale(Locale):

    names = ['ko', 'ko_kr']


# derived locale types & implementations.
class DutchLocale(Locale):

    names = ['nl', 'nl_nl']


class SlavicBaseLocale(Locale):
    
    def __init__(self):
        return

class BelarusianLocale(SlavicBaseLocale):

    names = ['be', 'be_by']


class PolishLocale(SlavicBaseLocale):

    names = ['pl', 'pl_pl']


class RussianLocale(SlavicBaseLocale):

    names = ['ru', 'ru_ru']


class UkrainianLocale(SlavicBaseLocale):

    names = ['ua', 'uk_ua']


class GermanLocale(Locale):

    names = ['de', 'de_de']


class AustriaLocale(Locale):

    names = ['de', 'de_at']


class NorwegianLocale(Locale):

    names = ['nb', 'nb_no']

    alarm = {
        'next': 'Neste alarm {0}',
        'none': '(ingen alarmer angitt)'
    }


class NewNorwegianLocale(NorwegianLocale):

    names = ['nn', 'nn_no']

    alarm = {
        'next': 'Neste alarm {0}',
        'none': '(ingen alarmer satt)'
    }


class PortugueseLocale(Locale):
    names = ['pt', 'pt_pt']
    
    
class BrazilianPortugueseLocale(PortugueseLocale):
    names = ['pt_br']


class TagalogLocale(Locale):

    names = ['tl']


class VietnameseLocale(Locale):

    names = ['vi', 'vi_vn']


class TurkishLocale(Locale):

    names = ['tr', 'tr_tr']


class ArabicLocale(Locale):

    names = ['ar', 'ar_eg']


class IcelandicLocale(Locale):

    names = ['is', 'is_is']


class DanishLocale(Locale):

    names = ['da', 'da_dk']


class MalayalamLocale(Locale):

    names = ['ml']


class HindiLocale(Locale):

    names = ['hi']


class CzechLocale(Locale):
    names = ['cs', 'cs_cz']


class FarsiLocale(Locale):

    names = ['fa', 'fa_ir']


class MacedonianLocale(Locale):
    names = ['mk', 'mk_mk']


class HebrewLocale(Locale):

    names = ['he', 'he_IL']


class MarathiLocale(Locale):

    names = ['mr']


def _map_locales():

    locales = {}

    for cls_name, cls in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(cls, Locale):
            for name in cls.names:
                locales[name.lower()] = cls  

    return locales

class CatalaLocale(Locale):
    names = ['ca', 'ca_ca']
    past = 'Fa {0}'
    future = '{0}' # I don't know what's the right phrase in catala for the future.

    timeframes = {
        'now': 'Ara mateix',
        'seconds': 'segons',
        'minute': '1 minut',
        'minutes': '{0} minuts',
        'hour': 'una hora',
        'hours': '{0} hores',
        'day': 'un dia',
        'days': '{0} dies',
        'month': 'un mes',
        'months': '{0} messos',
        'year': 'un any',
        'years': '{0} anys',
    }

    month_names = ['', 'Jener', 'Febrer', 'Març', 'Abril', 'Maig', 'Juny', 'Juliol', 'Agost', 'Setembre', 'Octubre', 'Novembre', 'Decembre']
    month_abbreviations = ['', 'Jener', 'Febrer', 'Març', 'Abril', 'Maig', 'Juny', 'Juliol', 'Agost', 'Setembre', 'Octubre', 'Novembre', 'Decembre']
    day_names = ['', 'Dilluns', 'Dimars', 'Dimecres', 'Dijous', 'Divendres', 'Disabte', 'Diumenge']
    day_abbreviations = ['', 'Dilluns', 'Dimars', 'Dimecres', 'Dijous', 'Divendres', 'Disabte', 'Diumenge']

class BasqueLocale(Locale):
    names = ['eu', 'eu_eu']
    past = 'duela {0}'
    future = '{0}' # I don't know what's the right phrase in Basque for the future.

    timeframes = {
        'now': 'Orain',
        'seconds': 'segundu',
        'minute': 'minutu bat',
        'minutes': '{0} minutu',
        'hour': 'ordu bat',
        'hours': '{0} ordu',
        'day': 'egun bat',
        'days': '{0} egun',
        'month': 'hilabete bat',
        'months': '{0} hilabet',
        'year': 'urte bat',
        'years': '{0} urte',
    }

    month_names = ['', 'Urtarrilak', 'Otsailak', 'Martxoak', 'Apirilak', 'Maiatzak', 'Ekainak', 'Uztailak', 'Abuztuak', 'Irailak', 'Urriak', 'Azaroak', 'Abenduak']
    month_abbreviations = ['', 'urt', 'ots', 'mar', 'api', 'mai', 'eka', 'uzt', 'abu', 'ira', 'urr', 'aza', 'abe']
    day_names = ['', 'Asteleehna', 'Asteartea', 'Asteazkena', 'Osteguna', 'Ostirala', 'Larunbata', 'Igandea']
    day_abbreviations = ['', 'al', 'ar', 'az', 'og', 'ol', 'lr', 'ig']


class HungarianLocale(Locale):

    names = ['hu', 'hu_hu']

    past = '{0} ezelőtt'
    future = '{0} múlva'

    timeframes = {
        'now': 'éppen most',
        'seconds': {
            'past': 'másodpercekkel',
            'future': 'pár másodperc'
        },
        'minute': {'past': 'egy perccel', 'future': 'egy perc'},
        'minutes': {'past': '{0} perccel', 'future': '{0} perc'},
        'hour': {'past': 'egy órával', 'future': 'egy óra'},
        'hours': {'past': '{0} órával', 'future': '{0} óra'},
        'day': {
            'past': 'egy nappal',
            'future': 'egy nap'
        },
        'days': {
            'past': '{0} nappal',
            'future': '{0} nap'
        },
        'month': {'past': 'egy hónappal', 'future': 'egy hónap'},
        'months': {'past': '{0} hónappal', 'future': '{0} hónap'},
        'year': {'past': 'egy évvel', 'future': 'egy év'},
        'years': {'past': '{0} évvel', 'future': '{0} év'},
    }

    month_names = ['', 'Január', 'Február', 'Március', 'Április', 'Május',
                   'Június', 'Július', 'Augusztus', 'Szeptember',
                   'Október', 'November', 'December']
    month_abbreviations = ['', 'Jan', 'Febr', 'Márc', 'Ápr', 'Máj', 'Jún',
                           'Júl', 'Aug', 'Szept', 'Okt', 'Nov', 'Dec']

    day_names = ['', 'Hétfő', 'Kedd', 'Szerda', 'Csütörtök', 'Péntek',
                 'Szombat', 'Vasárnap']
    day_abbreviations = ['', 'Hét', 'Kedd', 'Szer', 'Csüt', 'Pént',
                         'Szom', 'Vas']

    meridians = {
        'am': 'de',
        'pm': 'du',
        'AM': 'DE',
        'PM': 'DU',
    }

    def _format_timeframe(self, timeframe, delta):
        form = self.timeframes[timeframe]

        if isinstance(form, dict):
            if delta > 0:
                form = form['future']
            else:
                form = form['past']

        return form.format(abs(delta))


class ThaiLocale(Locale):

    names = ['th', 'th_th']

    past = '{0}{1}ที่ผ่านมา'
    future = 'ในอีก{1}{0}'

    timeframes = {
        'now': 'ขณะนี้',
        'seconds': 'ไม่กี่วินาที',
        'minute': '1 นาที',
        'minutes': '{0} นาที',
        'hour': '1 ชั่วโมง',
        'hours': '{0} ชั่วโมง',
        'day': '1 วัน',
        'days': '{0} วัน',
        'month': '1 เดือน',
        'months': '{0} เดือน',
        'year': '1 ปี',
        'years': '{0} ปี',
    }

    month_names = ['', 'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน',
                   'พฤษภาคม', 'มิถุนายน', 'กรกฏาคม', 'สิงหาคม',
                   'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
    month_abbreviations = ['', 'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.',
                           'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.',
                           'พ.ย.', 'ธ.ค.']

    day_names = ['', 'จันทร์', 'อังคาร', 'พุธ', 'พฤหัสบดี', 'ศุกร์',
                 'เสาร์', 'อาทิตย์']
    day_abbreviations = ['', 'จ', 'อ', 'พ', 'พฤ', 'ศ', 'ส', 'อา']

    meridians = {
        'am': 'am',
        'pm': 'pm',
        'AM': 'AM',
        'PM': 'PM',
    }

    BE_OFFSET = 543

    def year_full(self, year):
        '''Thai always use Buddhist Era (BE) which is CE + 543'''
        year += self.BE_OFFSET
        return '{0:04d}'.format(year)

    def year_abbreviation(self, year):
        '''Thai always use Buddhist Era (BE) which is CE + 543'''
        year += self.BE_OFFSET
        return '{0:04d}'.format(year)[2:]

    def _format_relative(self, humanized, timeframe, delta):
        '''Thai normally doesn't have any space between words'''
        if timeframe == 'now':
            return humanized
        space = '' if timeframe == 'seconds' else ' '
        direction = self.past if delta < 0 else self.future

        return direction.format(humanized, space)


_locales = _map_locales()
