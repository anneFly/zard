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
                    transform:  [ require('grunt-react').browserify ]
                }
            }
        },

        watch: {
            scripts: {
                files: ['client/js/**/*.jsx'],
                tasks: ['build'],
            }
        }

    });

    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-browserify');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('build', ['browserify', 'less']);

};
