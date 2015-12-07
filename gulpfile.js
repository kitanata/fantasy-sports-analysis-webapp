var gulp = require('gulp');
var sass = require('gulp-ruby-sass');

gulp.task('sass', function () {
    return sass('ackarma/static/sass/main.scss', {
            sourcemap: true,
            style: 'expanded'
        })
        .on('error', sass.logError)
        .pipe(gulp.dest('ackarma/static/css'));
});

gulp.task('watch', function() {
    gulp.watch('ackarma/static/sass/**/*.scss', ['sass']);
});

// Default Task
gulp.task('default', ['sass', 'watch']);

gulp.task('build', ['sass']);
