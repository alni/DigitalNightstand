var DigitalNightstandPlayer = (function (DigitalNightstand) {

    var last_key_down = -1;

    var KEY_CODES = {
        SPACE: 32,
        LEFT: 37,
        RIGHT: 39,
        UP: 38,
        DOWN: 40,
        PLAY_PAUSE: 179,
        VOLUME_UP: 175,
        VOLUME_DOWN: 174,
        PREVIOUS: 177,
        NEXT: 176
    };

    var obj = {
        init: function () {
            DigitalNightstand.fetchInitialData().done(function (data) {
                console.log(data.settings);
                console.log(data.countries);
                var context = {
                    countries: data.countries,
                    country: data.settings.radio.country
                };
                var source = $("#entry-template").html();
                var template = Handlebars.compile(source);
                var html = template(context);
                $("#countries").html(html).selectmenu( "refresh" );
            });
            // Change the current country for the station list
            $("#countries").on("change", function (e) {
                // This will only temporary change the chosen country.
                // To permanently change the country it must be changed from the
                // setup page
                $.get("/api/change_country/" + $(this).val()).done(function (data) {
                    $("#popupCountryChange").popup("open", {
                        positionTo: "#countries"
                    });
                    $("#station").text(data.radio.station);
                    $("#info").text(data.radio.info);
                });
            });

            // Call the API for button links with href that starts with "/api/"
            $(document).on("click", "a[href^='/api/']", function (e) {
                e.preventDefault();
                var $this = $(this);
                setTimeout(function () {
                    $this.removeClass("ui-btn-active");
                }, 250);

                // Call the API with the current href path
                $.getJSON($this.attr("href")).done(function (data) {
                    $("#station").text(data.radio.station);
                    $("#info").text(data.radio.info);
                });
            });

            $.getJSON("/api/list_stations").done(function (data) {
                //alert(data.length);
                var lang = navigator.language;
                var context = {
                    lang: navigator.language,
                    stations: data
                };
                var source = $("#station-list-template").html();
                var template = Handlebars.compile(source);
                var html = template(context);

                var message = DigitalNightstand.globalize(lang, "player/station_list/placeholder");
                $("#station-list-filter").attr("placeholder", message);
                $("#station-list").html(html).listview("refresh");
            });

            $(window).on("keydown", function (e) {
                if (last_key_down === -1 || +new Date() - last_key_down > 125) {
                    console.log(e.keyCode);
                    last_key_down = +new Date();
                    e.preventDefault();

                    switch (e.keyCode) {
                        case KEY_CODES.SPACE:
                        case KEY_CODES.PLAY_PAUSE:
                            $("#play").trigger("click");
                            break;
                        case KEY_CODES.LEFT:
                        case KEY_CODES.VOLUME_DOWN:
                            $("#vol_down").trigger("click");
                            break;
                        case KEY_CODES.RIGHT:
                        case KEY_CODES.VOLUME_UP:
                            $("#vol_up").trigger("click");
                            break;
                        case KEY_CODES.UP:
                        case KEY_CODES.NEXT:
                            $("#station_next").trigger("click");
                            break;
                        case KEY_CODES.DOWN:
                        case KEY_CODES.PREVIOUS:
                            $("#station_next").trigger("click");
                            break;
                    }
                }
            });
        },

        updateInfo: function () {
            $.getJSON("/api/").done(function (data) {
                $("#station").text(data.radio.station);
                $("#info").text(data.radio.info);
            });
        }
    };

    return obj;
})(DigitalNightstand);
