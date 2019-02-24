# Digital Nightstand #

Digital Nightstand for the Tingbot/Raspberry Pi.

Features includes:

* Weather Forecast,
* Digital Clock
* Alarm Clock
* Web Frontend
* Translated into:
  * English (en)
  * Norwegian Bokmal (nb)
  * Norwegian Nynorsk (nn)

## Button shortcuts ##

Button            | Action
----------------- | ---------------------
`midright`        | Snooze current alarm
`right`           | Take screenshot


## Keyboard shortcuts ##

Key               | Action
----------------- | ---------------------
<kbd>F1</kbd>     | Switch to Radio Page
<kbd>F2</kbd>     | Switch to Clock Page
<kbd>Space</kbd>  | Pause/Play
<kbd>&larr;</kbd> | Volume Down
<kbd>&rarr;</kbd> | Volume Up
<kbd>&uarr;</kbd> | Next station
<kbd>&darr;</kbd> | Previous station


## Weather Forecast ##

Get weather forecast for a place on Earth.

Currently supports:

* Display current weather conditions on the Clock page - summary, temperature and icon
* Displaying the summary in different languages
* Display the temperature by different units - location dependent or user set

> **[Powered by Dark Sky](https://darksky.net/poweredby/ "Powered by Dark Sky")**

## Digital Clock ##

Shows the current time and date. The time is shown big, and the date medium size but still readable.

The time and date is formatted based on the locale of the computer.

Also shows the next scheduled alarm (if any).

## Alarms ##

Supports configurable alarms from a JSON file.

The alarms can have a customized `title`, `time`, `repeat`, and `days`.

Easily set-up from the Web Frontend.

## Web Frontend ##

The Web Frontend provides configuration and control of the Nightstand from a web browser.

Accepts connections default on port `8000`.

Supports:

* Setting up the alarms (total 5)
* Setting up the weather forecast (including latitude/longitude coordinates, desired language and units)

## Configuration and Data Files ##

The configuration and data files are stored within a specific folder path unique for each platform.

* `config.json` - contains all user configured settings. This includes all settings configured with the Web Frontend (excluding the _Dark Sky API Key_)
* `weather/private.json` - contains private user data that should not be shared. This includes the Dark Sky API Key set from the Web Frontend

### Dark Sky API Key ###

When downloaded weather data using the weather forecast service, a Dark Sky API Key must be provided.

This can be set from the Web Frontend.

When the value of Dark Sky API Key field is changed the API Key is
automatically saved to `weather/private.json`. If successful the field is cleared to prevent reading of the API key.

The Dark Sky API Key is never loaded to the configuration page.

--------

## Acknowledgements ##

This application has been inspired, and contains/uses other projects.

* Background [image][background-image] by [skeeze][pixabay-skeeze] from [Pixabay][pixabay]
* Color palette was generated from the background image with the [Pictaculous][pictaculous] service

### Python libraries ###

This project uses the following Python libraries:

* `appdirs` - [`appdirs`][appdirs] is created by [ActiveState Software Inc][activestate-software-inc] and distributed under the [MIT license][appdirs-license]
* `arrow` - [`arrow`][arrow] is created by [Chris Smith][chris-smith] and licensed under the [Apache License, Version 2.0][apache-license-2-0]
* `pygame` - [`pygame`][pygame] is developed by the [Pygame Community][pygame-community] and distributed under [GNU LGPL version 2.1][pygame-license]
* `python-forecastio` - [`python-forecastio`][python-forecastio] is created by [Ze'ev Gilovitz][ZeevG] and licensed under the ['BSD 2-clause license'][python-forecastio-license]
* `schedule` - [`schedule`][schedule] is created by [Daniel Bader][daniel-bader] and distributed under the [MIT license][schedule-license]
* `tingbot-python` - [`tingbot-python`][tingbot-python] is created by [Tingbot][tingbot] and licensed under the ['BSD 2-clause license'][tingbot-python-license]

### Alarm ###

Uses [Material][material-alarm-sounds] alarm sounds from the [`platforms_frameworks_base`][platforms-frameworks-base] repository by
[The Android Open Source Project][aosp].

### The Web Frontend ###

Built with [jQuery Mobile][jqm] by [jQuery Foundation, Inc.][jquery-foundation] released under the [MIT license][jqm-license].

Uses the [nativeDroid2][nativeDroid2] template by [Raphael Wildhaber, Godesign Webpublishing GmbH][wildhaber] released under the [MIT license][nativeDroid2-license].

Also uses the [DateBox][jtsage-datebox] JavaScript library by [J.T. Sage][jtsage] released under the [MIT license][jtsage-datebox-license].


[background-image-old]: https://pixabay.com/en/banner-header-lines-light-rays-911778/ "background image"
[pixabay-geralt]: https://pixabay.com/en/users/geralt-9301/ "geralt"
[background-image]: https://pixabay.com/en/delicate-arch-night-stars-landscape-960279/ "background image"
[pixabay-skeeze]: https://pixabay.com/en/users/skeeze-272447/ "skeeze"
[pixabay]: https://pixabay.com/ "Pixabay"
[pictaculous]: http://pictaculous.com/ "Pictaculous"

[appdirs]: https://github.com/ActiveState/appdirs
[activestate-software-inc]: http://www.activestate.com/ "ActiveState Software Inc"
[appdirs-license]: https://github.com/ActiveState/appdirs/blob/master/LICENSE.txt "MIT license"
[arrow]: https://github.com/crsmithdev/arrow/
[chris-smith]: https://github.com/crsmithdev "Chris Smith"
[apache-license-2-0]: http://www.apache.org/licenses/LICENSE-2.0 "Apache License, Version 2.0"
[pygame]: http://www.pygame.org/
[pygame-community]: http://www.pygame.org/ "Pygame Community"
[pygame-license]: http://www.gnu.org/copyleft/lesser.html "GNU LGPL version 2.1"
[schedule]: https://github.com/dbader/schedule
[python-forecastio]: https://github.com/ZeevG/python-forecast.io "Dark Sky Wrapper"
[ZeevG]: http://zeevgilovitz.com/ "Ze'ev Gilovitz"
[python-forecastio-license]: https://github.com/ZeevG/python-forecast.io/blob/master/LICENSE.txt "BSD 2-clause license"
[daniel-bader]: https://twitter.com/dbader_org "Daniel Bader"
[schedule-license]: https://github.com/dbader/schedule/blob/master/LICENSE.txt "MIT license"
[tingbot-python]: https://github.com/tingbot/tingbot-python
[tingbot]: http://tingbot.com/ "Tingbot"
[tingbot-python-license]: https://github.com/tingbot/tingbot-python/blob/master/LICENSE "BSD 2-clause license"
[material-alarm-sounds]: https://github.com/android/platform_frameworks_base/tree/master/data/sounds/alarms/material/ogg "Material alarm sounds"
[platforms-frameworks-base]: https://github.com/android/platform_frameworks_base "platforms frameworks base"
[aosp]: http://source.android.com/ "The Android Open Source Project"
[material-icons]: https://github.com/google/material-design-icons/ "Material design icons"
[jqm]: http://jquerymobile.com/ "jQuery Mobile"
[jquery-foundation]: https://jquery.org/ "jQuery Foundation, Inc."
[jqm-license]: https://github.com/jquery/jquery-mobile/blob/master/LICENSE.txt "MIT license"
[nativeDroid2]: http://nativedroid.godesign.ch/ "nativeDroid2"
[wildhaber]: http://godesign.ch/ "Raphael Wildhaber, Godesign Webpublishing GmbH"
[nativeDroid2-license]: https://github.com/wildhaber/nativeDroid2/blob/master/LICENSE "MIT license"
[jtsage-datebox]: https://github.com/jtsage/jquery-mobile-datebox "Datebox"
[jtsage]: https://github.com/jtsage "J.T. Sage"
[jtsage-datebox-license]: https://github.com/jtsage/jquery-mobile-datebox/blob/master/LICENSE.txt "MIT license"
