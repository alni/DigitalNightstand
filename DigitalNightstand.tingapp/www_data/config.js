var DigitalNightstandSetup = (function (DigitalNightstand) {

    var obj = {
        init: function () {
            DigitalNightstand.fetchInitialData().done(function (data) {
                console.log(data.settings);
                console.log(data.countries);
                var context = data.settings || {
                    alarms: [{
                        // #1
                    }, {
                        // #2
                    }, {
                        // #3
                    }, {
                        // #4
                    }, {
                        // #5
                    }],
                    radio: {
                        country: "NO",
                        radio_stations: []
                    },
                    general: {
                        config_file: "config.json",
                        mplayer_path: "mplayer"
                    }
                };
                context.radio.countries = data.countries || [{
                    country_code: "GB",
                    name: "United Kingdom"
                }, {
                    country_code: "NO",
                    name: "Norway"
                }];
                var alarms_length = context.alarms.length; // Configured alarms
                if (context.alarms.length < 5) {
                    // If the number of current configured alarms is less than 5, 
                    // append extra, un-configured, alarms so that the number of 
                    // alarms is a total of 5
                    for (var i = context.alarms.length; i < 5; i++) {
                        context.alarms.push([]);
                    }
                }
                var num_alarms = context.alarms.length; // All alarms
                var source = $("#entry-template").html();
                var template = Handlebars.compile(source);
                var html = template(context);
                $("#form").html(html);

                // Only loop through configured alarms
                for (var i = 0; i < alarms_length; i++) {
                    var alarm = context.alarms[i];
                    var $time = $("#alarm_" + i + "_time");
                    var $repeat = $("#alarm_" + i + "_repeat");
                    $time.val(pad(alarm.time[0], 2) + ":" + pad(alarm.time[1], 2));
                    if (!!alarm.repeat) {
                        $repeat.attr("checked", "checked").trigger("change");
                    }
                    if (alarm.days && alarm.days.length > 0) {
                        $("input[name='alarm_" + i + "_days']").each(function (index, elem) {
                            var $this = $(this);
                            if ($.inArray($this.val(), alarm.days) > -1) {
                                $this.attr("checked", "checked").trigger("change");
                            }
                        });
                    }
                }
                $("#form").trigger("create");
                $("#dirble_api_key").on("change", function (e) {
                    var $this = $(this);
                    var val = $this.val();
                    if (val && val.length > 0) {
                        // Send and save the key to the main application
                        $.post("/dirble_api_key", JSON.stringify({
                            // Base64 encode the key before sending it
                            dirble_api_key: btoa(val)
                        })).done(function () {
                            // Clear the field to prevent reading of the API key
                            $this.val("");
                        });
                    }
                });
                $("#form").on("submit", function (e) {
                    e.preventDefault();
                    var alarms = [];
                    for (var i = 0; i < num_alarms; i++) {
                        var $time = $("#alarm_" + i + "_time");
                        var $hour = $("#alarm_" + i + "_hour");
                        var $min = $("#alarm_" + i + "_min");
                        var $title = $("#alarm_" + i + "_title");
                        var $days = $("input[name='alarm_" + i + "_days']:checked");
                        var $repeat = $("#alarm_" + i + "_repeat:checked");

                        if ($time.val()) {
                            var time = $time.val().split(":");
                            var hour = parseInt(time[0], 10);
                            var min = parseInt(time[1], 10);
                            var obj = {
                                repeat: !!$repeat.length,
                                time: [hour, min],
                                //time: [+$hour.val(), +$min.val()],
                                title: $title.val() || "ALARM",
                            };
                            if ($days.length > 0) {
                                obj.days = [];
                                $days.each(function (index) {
                                    obj.days[index] = $(this).val();
                                });
                            }
                            alarms.push(obj);
                        }
                    }

                    console.log(alarms);
                    var radio = {
                        country: $("#radio_stations_country").val(),
                        radio_stations: []
                    };
                    var radio_custom_stations = $("#radio_custom_stations").val().trim().split("\n");
                    if (radio_custom_stations.length > 0) {
                        radio_custom_stations = radio_custom_stations.map(function (line, index) {
                            return {
                                name: "Custom #" + (index + 1),
                                groups: ["Custom"],
                                stream_uri: line + ""
                            };
                        });
                    } else {
                        radio_custom_stations = [];
                    }
                    radio.radio_stations.concat(radio_custom_stations);

                    $.post("/", JSON.stringify({
                        alarms: alarms,
                        radio: radio
                        //radio_stations: radio_custom_stations
                    }));

                });
            });
        }
    };

    return obj;
})(DigitalNightstand);
