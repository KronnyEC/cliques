module.exports = function (grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    ngmin: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      main: {
        files: {
          'build/cliques.min.js': [
            'js/app.js',
            'js/controllers.js'
          ]
        }
      }
    },
    csslint: {
      options: {
        force: true,
        absoluteFilePathsForFormatters: true,
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n',
        "important": false,
        "unqualified-attributes": false

      },
      lax: {
        options: {
          import: false
        },
        src: ['css/*.css', '!css/*.min.css']
      }
    },
    cssmin: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      }
//      combine: {
//        files: {
//          'build/cliques.min.css': [
//
//            'bower_components/foundation/css/foundation.css',
//            'bower_components/foundation/css/normalize.css',
//            'css/cliques.css'
//          ]
//        }
//      }
    },
    htmlangular: {
      html: {
        options: {
          customtags: [
            'chat',
            'post'
          ]
        },
        files: {
          src: ['index.html', 'templates/*.html', 'partials/*.html']
        }
      }
    },
    ngconstant: {
      options: {
        name: 'cliques_config',
        wrap: '"use strict";\n\n{%= __ngModule %}',
        space: '  '
      },
      development: {
        options: {
          dest: 'js/cliques_config.js'
        },
        constants: {
          ENV: 'development',
          BACKEND_SERVER: 'http://127.0.0.1:8080/api/v1/'
        }
      },
      production: {
        options: {
          dest: 'build/cliques_config.js'
        },
        constants: {
          ENV: 'production',
          BACKEND_SERVER: 'http://www.slashertraxx.com/api/v1/'
        }
      }
    },
    copy: {
      html: {
        files: [
          // includes files within path
          {
            expand: true,
            src: ['index.html'],
            dest: 'build/'
          },
          {
            expand: true,
            src: ['partials/*.html'],
            dest: 'build/partials/'
          },
          {
            expand: true,
            src: ['templates/*.html'],
            dest: 'build/templates/'
          }
        ]
      }
    },
    useminPrepare: {
      html: 'index.html',
      options: {
        dest: 'build'
      }
    },
    usemin: {
      html: 'build/index.html'
    },
    clean: {
      release: ['build/*']
    },
    concat: {
      options: {
        concat: 'generated'
      }
    }

  });

  // Tasks
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-csslint');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-ngmin');
  grunt.loadNpmTasks('grunt-html-angular-validate');
  grunt.loadNpmTasks('grunt-ng-constant');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-usemin');
  grunt.loadNpmTasks('grunt-filerev');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-copy');

  grunt.registerTask('build', [
    'useminPrepare',
    'concat:generated',
    'cssmin:generated',
    'ngmin',
    'uglify:generated',
    'filerev',
    'usemin'
  ]);

  // Default task(s).
  grunt.registerTask('default', [
    'clean',
    'ngconstant',
    'csslint',
    'useminPrepare',
    'concat:generated',
    'cssmin:generated',
    'ngmin',
    'uglify:generated',
    'copy',
//    'filerev',
    'usemin'
  ]);

};
