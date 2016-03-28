# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import calendar
import inspect
import sys


def get_locale(name):
    '''Returns an appropriate :class:`Locale <locale.Locale>` corresponding
    to an input locale name.

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

    title = 'Digital Nightstand'

    fetching_new_data = "Fetching new data..."

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

    # The Finnish grammar is very complex, and its hard to convert
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

    title = 'Digitalt Nattbord'

    fetching_new_data = "Henter ny data..."

    alarm = {
        'next': 'Neste alarm {0}',
        'none': '(ingen alarmer angitt)'
    }


class NewNorwegianLocale(NorwegianLocale):

    names = ['nn', 'nn_no']

    fetching_new_data = "Henter ny data..."

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


class BasqueLocale(Locale):
    names = ['eu', 'eu_eu']


class HungarianLocale(Locale):

    names = ['hu', 'hu_hu']


class ThaiLocale(Locale):

    names = ['th', 'th_th']


_locales = _map_locales()
