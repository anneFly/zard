module.exports = function (grunt) {
    grunt.initConfig({

        compass: {
            dev: {
                options: {
                    config: 'config.rb'
                }
            }
        },

        browserify: {
            dev: {
                files: {
                    '../statics/js/bundle.js': ['js/**/*.js', 'js/**/*.jsx']
                },
                options: {
                    transform:  [ require('grunt-react').browserify ]
                }
            }
        }

    });

    grunt.loadNpmTasks('grunt-contrib-compass');
    grunt.loadNpmTasks('grunt-browserify');

    grunt.registerTask('build', ['compass', 'browserify']);

};
