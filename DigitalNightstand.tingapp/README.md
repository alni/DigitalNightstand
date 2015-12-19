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

### The Radio ###

The radio layout has been inspired heavily by the **[Raspberry Pi radio player with touchscreen][raspberry-pi-radio-player-with-touchscreen]** by [Spencer Organ][adafruit-learn-Uktechreviews] from the [Adafruit Learning System][adafruit-learn]

Uses icons from the [Material design icons][material-icons] by Google, Inc

### Alarm ###

Uses [Material][material-alarm-sounds] alarm sounds from the [`platforms_frameworks_base`][platforms-frameworks-base] repository by [The Android Open Source Project][aosp]


[background-image]: https://pixabay.com/en/banner-header-lines-light-rays-911778/ "background image"
[pixabay-geralt]: https://pixabay.com/en/users/geralt-9301/ "geralt"
[pixabay]: https://pixabay.com/ "Pixabay"
[pictaculous]: http://pictaculous.com/ "Pictaculous"
[raspberry-pi-radio-player-with-touchscreen]: https://learn.adafruit.com/raspberry-pi-radio-player-with-touchscreen/overview "Raspberry Pi radio player with touchscreen"
[adafruit-learn-Uktechreviews]: https://learn.adafruit.com/users/Uktechreviews "Spencer Organ"
[adafruit-learn]: https://learn.adafruit.com/ "Adafruit Learning System"
[material-alarm-sounds]: https://github.com/android/platform_frameworks_base/tree/master/data/sounds/alarms/material/ogg "Material alarm sounds"
[platforms-frameworks-base]: https://github.com/android/platform_frameworks_base "platforms frameworks base"
[aosp]: http://source.android.com/ "The Android Open Source Project"
[material-icons]: https://github.com/google/material-design-icons/ "Material design icons"