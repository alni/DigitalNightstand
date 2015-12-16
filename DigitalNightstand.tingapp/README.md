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

Supports:

* Radio Player control
* Setting up the alarms (total 5)
* Adding custom internet radio stations

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