var DigitalNightstand = (function () {
    var obj = {
        fetchInitialData : function () {
            var promise = $.Deferred();
            $.when(
                $.getJSON("/api/config"),
                $.getJSON("/api/list_countries")
            ).done(function (settings, countries) {
                promise.resolve({
                    settings: settings[0],
                    countries: countries[0]
                });
            });
            return promise;
        }
    };

    return obj;
})();

