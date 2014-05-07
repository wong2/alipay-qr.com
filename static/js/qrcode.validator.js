(function($) {
  $.fn.bootstrapValidator.validators.qrcode = {
    validate: function(validator, $field, options) {
      if (!window.FileReader) {
        return true;
      }

      var dfd = new $.Deferred()
        , files = $field.get(0).files
        , file = files[0];

      qrcode.callback = function(data) {
        var result = !!data;
        if (options.regex) {
          result = options.regex.test(data);
        }
        if (data == 'error decoding QR Code') {
          result = false;
        }
        dfd.resolve($field, 'qrcode', result);
      };

      var reader = new FileReader();
      reader.onload = function(e) {
        qrcode.decode(e.target.result);
      };
      reader.readAsDataURL(file);

      return dfd;
    }
  };
}(window.jQuery));
