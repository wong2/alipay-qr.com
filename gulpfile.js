var gulp = require('gulp'),
    concat = require('gulp-concat'),
    uglify = require('gulp-uglify');


gulp.task('validator', function() {
  gulp.src(['static/js/bootstrapValidator.js', 'static/js/qrdecoder.js', 'qrdecoder.js/qrcode.validator.js'])
    .pipe(uglify())
    .pipe(concat('validator.min.js'))
    .pipe(gulp.dest('./static/js/'))
});
