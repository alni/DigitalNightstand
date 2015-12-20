# Digital Nightstand #

Digital Nightstand for the Tingbot/Raspberry Pi.

Features includes:

* Internet Radio, 
* Digital Clock
* Alarm Clock
* Web Frontend

## Internet Radio ##

Listen to Internet Radio stations.

Currently supports:

* `NRK Radio` - <http://lyd.nrk.no> (Norwegian Broadcasting Corporation/Norsk rikskringkasting AS)
* Downloading list of radio stations by country with the [Dirble][dirble] service
* Custom radio stations


## Digital Clock ##

Shows the current time and date. The time is shown big, and the date medium size but still readable.

## Alarms ##

Supports configurable alarms from a JSON file.

The alarms can have a customized `title`, `days`, and `time`.

## Web Frontend ##

The Web Frontend provides configuration and control of the Nightstand from a web browser.

Accepts connections default on port `8000`.

Supports:

* Radio Player control
* Setting up the alarms (total 5)
* Adding custom internet radio stations

## Configuration and Data Files ##

The configuration and data files are stored within a specific folder path unique for each platform.

* `config.json` - contains all user configured settings. This includes all settings configured with the Web Frontend (excluding the _Dirble API Key_)
* `radio/<country>.json`  - contains transformed internet stations data downloaded from Dirble a specific `country`
* `radio/private.json` - contains private user data that should not be shared. This includes the Dirble API Key set from the Web Frontend

### Dirble API Key ###

When downloaded radio channels using the Dirble Service, a Dirble API Key must be provided.

This can be set from the Web Frontend.

When the value of Dirble API Key field is changed the API Key is automatically saved to `radio/private.json`. If successful the field is cleared to prevent reading of the API key.

The Dirble API Key is never loaded to the configuration page.

--------

## Acknowledgements ##

This app has been inspired, and contains/uses other projects.

* Background [image][background-image] by [geralt][pixabay-geralt] from [Pixabay][pixabay]
* Color palette was generated from the background image with the [Pictaculous][pictaculous] service

### Python libraries ###

This project uses the following Python libraries:

* `appdirs` - [`appdirs`][appdirs] is created by [ActiveState Software Inc][activestate-software-inc] and distributed under the [MIT license][appdirs-license]
* `arrow` - [`arrow`][arrow] is created by [Chris Smith][chris-smith] and licensed under the [Apache License, Version 2.0][apache-license-2-0]
* `pygame` - [`pygame`][pygame] is created by the [Pygame Community][pygame-community] and distributed under [GNU LGPL version 2.1][pygame-license]
* `schedule` - [`schedule`][schedule] is created by [Daniel Bader][daniel-bader] and distributed under the [MIT license][schedule-license]
* `tingbot-python` - [`tingbot-python`][tingbot-python] is created by [Tingbot][tingbot] and licensed under the ['BSD 2-clause license'][tingbot-python-license]

### The Radio ###

The radio layout has been inspired heavily by the **[Raspberry Pi radio player with touchscreen][raspberry-pi-radio-player-with-touchscreen]** by [Spencer Organ][adafruit-learn-Uktechreviews] from the [Adafruit Learning System][adafruit-learn]

Uses icons from the [Material design icons][material-icons] by Google, Inc

### Alarm ###

Uses [Material][material-alarm-sounds] alarm sounds from the [`platforms_frameworks_base`][platforms-frameworks-base] repository by [The Android Open Source Project][aosp]


[dirble]: https://dirble.com/ "Dirble"
[background-image]: https://pixabay.com/en/banner-header-lines-light-rays-911778/ "background image"
[pixabay-geralt]: https://pixabay.com/en/users/geralt-9301/ "geralt"
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
[daniel-bader]: https://twitter.com/dbader_org "Daniel Bader"
[schedule-license]: https://github.com/dbader/schedule/blob/master/LICENSE.txt "MIT license"
[tingbot-python]: https://github.com/tingbot/tingbot-python
[tingbot]: http://tingbot.com/ "Tingbot"
[tingbot-python-license]: https://github.com/tingbot/tingbot-python/blob/master/LICENSE "BSD 2-clause license"
[raspberry-pi-radio-player-with-touchscreen]: https://learn.adafruit.com/raspberry-pi-radio-player-with-touchscreen/overview "Raspberry Pi radio player with touchscreen"
[adafruit-learn-Uktechreviews]: https://learn.adafruit.com/users/Uktechreviews "Spencer Organ"
[adafruit-learn]: https://learn.adafruit.com/ "Adafruit Learning System"
[material-alarm-sounds]: https://github.com/android/platform_frameworks_base/tree/master/data/sounds/alarms/material/ogg "Material alarm sounds"
[platforms-frameworks-base]: https://github.com/android/platform_frameworks_base "platforms frameworks base"
[aosp]: http://source.android.com/ "The Android Open Source Project"
[material-icons]: https://github.com/google/material-design-icons/ "Material design icons"
