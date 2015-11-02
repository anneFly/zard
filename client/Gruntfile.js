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
        },

        watch: {
            scripts: {
                files: ['js/**/*.jsx', 'scss/**/*.scss'],
                tasks: ['build'],
            }
        }

    });

    grunt.loadNpmTasks('grunt-contrib-compass');
    grunt.loadNpmTasks('grunt-browserify');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('build', ['compass', 'browserify']);

};
