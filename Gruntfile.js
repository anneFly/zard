module.exports = function (grunt) {
    grunt.initConfig({

        less: {
            dev: {
                options: {
                    compress: true
                },
                files: {
                    'statics/css/styles.css': 'client/less/styles.less'
                }
            }
        },

        browserify: {
            dev: {
                files: {
                    'statics/js/bundle.js': ['client/js/**/*.js', 'client/js/**/*.jsx']
                },
                options: {
                    transform: [['babelify', {presets: ['react', 'es2015']}]],
                }
            }
        },

        watch: {
            scripts: {
                files: ['client/js/**/*.jsx', 'client/js/**/*.js'],
                tasks: ['build'],
            }
        }

    });

    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-browserify');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('build', ['browserify', 'less']);

};
