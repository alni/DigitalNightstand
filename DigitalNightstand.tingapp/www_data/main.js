var DigitalNightstand = (function () {
    var lang = navigator.language;
    // At this point, we have Globalize loaded. But, before we can use it, we
    // need to feed it on the appropriate I18n content (Unicode CLDR). In order
    // to do so, we use `Globalize.load()` and pass the content. On this demo,
    // we made the things a little easier for you: we've embedded static JSON
    // into the demo. So, you don't need to actually fetch it elsewhere.
    Globalize.load({
        //"main": {
        //    "en": {
        //        "identity": {
        //            "version": {
        //                "_cldrVersion": "25",
        //                "_number": "$Revision: 91 $"
        //            },
        //            "generation": {
        //                "_date": "$Date: 2014-03-13 22:27:12 -0500 (Thu, 13 Mar 2014) $"
        //            },
        //            "language": "en"
        //        },
        //        "dates": {
        //            "calendars": {
        //                "gregorian": {
        //                    "months": {
        //                        "format": {
        //                            "abbreviated": {
        //                                "1": "Jan",
        //                                "2": "Feb",
        //                                "3": "Mar",
        //                                "4": "Apr",
        //                                "5": "May",
        //                                "6": "Jun",
        //                                "7": "Jul",
        //                                "8": "Aug",
        //                                "9": "Sep",
        //                                "10": "Oct",
        //                                "11": "Nov",
        //                                "12": "Dec"
        //                            }
        //                        }
        //                    },
        //                    "dayPeriods": {
        //                        "format": {
        //                            "wide": {
        //                                "am": "AM",
        //                                "am-alt-variant": "am",
        //                                "noon": "noon",
        //                                "pm": "PM",
        //                                "pm-alt-variant": "pm"
        //                            }
        //                        }
        //                    },
        //                    "dateFormats": {
        //                        "medium": "MMM d, y"
        //                    },
        //                    "timeFormats": {
        //                        "medium": "h:mm:ss a",
        //                    },
        //                    "dateTimeFormats": {
        //                        "medium": "{1}, {0}"
        //                    }
        //                }
        //            },
        //            "fields": {
        //                "second": {
        //                    "displayName": "Second",
        //                    "relative-type-0": "now",
        //                    "relativeTime-type-future": {
        //                        "relativeTimePattern-count-one": "in {0} second",
        //                        "relativeTimePattern-count-other": "in {0} seconds"
        //                    },
        //                    "relativeTime-type-past": {
        //                        "relativeTimePattern-count-one": "{0} second ago",
        //                        "relativeTimePattern-count-other": "{0} seconds ago"
        //                    }
        //                }
        //            }
        //        },
        //        "numbers": {
        //            "currencies": {
        //                "USD": {
        //                    "symbol": "$"
        //                }
        //            },
        //            "defaultNumberingSystem": "latn",
        //            "symbols-numberSystem-latn": {
        //                "decimal": ".",
        //                "exponential": "E",
        //                "group": ",",
        //                "infinity": "∞",
        //                "minusSign": "-",
        //                "nan": "NaN",
        //                "percentSign": "%",
        //                "perMille": "‰",
        //                "plusSign": "+",
        //                "timeSeparator": ":"
        //            },
        //            "decimalFormats-numberSystem-latn": {
        //                "standard": "#,##0.###"
        //            },
        //            "currencyFormats-numberSystem-latn": {
        //                "currencySpacing": {
        //                    "beforeCurrency": {
        //                        "currencyMatch": "[:^S:]",
        //                        "surroundingMatch": "[:digit:]",
        //                        "insertBetween": " "
        //                    },
        //                    "afterCurrency": {
        //                        "currencyMatch": "[:^S:]",
        //                        "surroundingMatch": "[:digit:]",
        //                        "insertBetween": " "
        //                    }
        //                },
        //                "standard": "¤#,##0.00"
        //            }
        //        }
        //    }
        //},
        "supplemental": {
            "version": {
                "_cldrVersion": "25",
                "_number": "$Revision: 91 $"
            },
            "currencyData": {
                "fractions": {
                    "DEFAULT": {
                        "_rounding": "0",
                        "_digits": "2"
                    }
                }
            },
            "likelySubtags": {
                "en": "en-Latn-US",
                "nb": "nb-Latn-NO",
            },
            "plurals-type-cardinal": {
                "en": {
                    "pluralRule-count-one": "i = 1 and v = 0 @integer 1",
                    "pluralRule-count-other": " @integer 0, 2~16, 100, 1000, 10000, 100000, 1000000, … @decimal 0.0~1.5, 10.0, 100.0, 1000.0, 10000.0, 100000.0, 1000000.0, …"
                },
                "nb": {
                    "pluralRule-count-one": "i = 1 and v = 0 @integer 1",
                    "pluralRule-count-other": " @integer 0, 2~16, 100, 1000, 10000, 100000, 1000000, … @decimal 0.0~1.5, 10.0, 100.0, 1000.0, 10000.0, 100000.0, 1000000.0, …"
                }
            }
        }
    });
    var _globalize = function (lang, message, params, options) {
        var formatter = Globalize(lang).messageFormatter(message);
        return formatter([params]);
    };
    var lang = navigator.language;
    Handlebars.registerHelper("globalize", function (lang, message, params, options) {
        return _globalize(lang, message, params);
    });
    var obj = {
        fetchInitialData : function () {
            var promise = $.Deferred();
            $.when(
                $.getJSON("/api/config"),
                //$.getJSON("/api/list_countries"),
                $.getJSON("/data/messages.json")
            ).done(function (settings, messages) { //countries, messages) {
                var _settings = settings[0];
                Globalize.loadMessages(messages[0]);
                _settings.lang = lang + "";
                $("[data-globalize]").each(function () {
                    var $this = $(this);
                    var formatter = Globalize(lang).messageFormatter($this.data("globalize"));
                    $this.text(formatter());
                });
                promise.resolve({
                    settings: _settings//,
                    //countries: countries[0]
                });
            });
            return promise;
        },
        globalize: (function () {
            return _globalize;
        })()
    };

    return obj;
})();
