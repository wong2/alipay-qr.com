var gulp = require('gulp'),
    concat = require('gulp-concat'),
    uglify = require('gulp-uglify'),
    rename = require('gulp-rename'),
    mincss = require('gulp-minify-css');

gulp.task('js', function() {
  gulp.src(['static/js/bootstrap.file-input.js'])
    .pipe(uglify())
    .pipe(rename({suffix: '.min'}))
    .pipe(gulp.dest('./static/js/'))
});

gulp.task('validator.js', function() {
  gulp.src(['static/js/bootstrapValidator.js', 'static/js/qrdecoder.js', 'qrdecoder.js/qrcode.validator.js'])
    .pipe(uglify())
    .pipe(concat('validator.min.js'))
    .pipe(gulp.dest('./static/js/'))
});

gulp.task('css', function() {
  gulp.src(['static/css/flat-ui.css'])
    .pipe(mincss())
    .pipe(rename({suffix: '.min'}))
    .pipe(gulp.dest('./static/css/'))
});

gulp.task('default', ['js', 'validator.js', 'css'])
