module.exports = function (grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    ngAnnotate: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      generated: {
        files: {
          'build/js/cliques.min.js': [
            '.tmp/concat/js/cliques.min.js'
          ],
          'build/js/angular.min.js': [
            '.tmp/concat/js/angular.min.js'
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
        src: [ 'css/*.css', '!css/*.min.css']
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
          dest: 'js/cliques_config.js'
        },
        constants: {
          ENV: 'production',
          BACKEND_SERVER: 'http://www.slashertraxx.com/api/v1/'
        }
      }
    },
    copy: {
      generated: {
        files: [
          // includes files within path
          {
            expand: true,
            src: ['index.html'],
            dest: 'build/'
          },
          {
            expand: true,
            src: ['spec.html'],
            dest: 'build/'
          },
          {
            expand: true,
            src: ['icon.png'],
            dest: 'build/'
          },
          {
            expand: true,
            src: ['config.xml'],
            dest: 'build/'
          },
          {
            expand: true,
            src: ['spec/*'],
            dest: 'build/spec/'
          },
          {
            expand: true,
            src: ['res/*'],
            dest: 'build/res/*'
          },
          {
            expand: true,
            src: ['partials/*.html'],
            dest: 'build/'
          },
          {
            expand: true,
            src: ['templates/*.html'],
            dest: 'build/'
          },
          {
            src: ['.tmp/concat/js/cliques.min.js'],
            dest: 'build/js/cliques.min.js'
          }
        ]
      },
      www: {
        files: [
          {
            expand: true,
            src: ['**'],
            cwd: 'build',
            dest: '../web'
          }
//          {
//            cwd: 'build/js',
//            src: ['**'],
//            dest: '../www/js'
//          },
//          {
//            cwd: 'build/css',
//            src: ['**'],
//            dest: '../www/css'
//          },
//          {
//            cwd: 'build/partials',
//            src: ['**'],
//            dest: '../www/partials'
//          },
//          {
//            cwd: 'build/templates',
//            src: ['**'],
//            dest: '../www/templates'
//          },
//          {
//            src: ['build/index.html'],
//            dest: '../www/index.html'
//          }
        ]
      },
      app: {
        files: [
          {
            expand: true,
            src: ['**'],
            cwd: 'build',
            dest: '../cordova/www'
          }

        ]
      }
    },
    useminPrepare: {
      html: 'index.html',
      options: {
        dest: 'build/'
      }
    },
    usemin: {
      html: 'build/index.html'
    },
    clean: {
      build: ['build/*']
    },
    concat: {
      options: {
        concat: 'generated'
      }
    },
    cordovacli: {
      options: {
        path: '../cordova/www'
      },
      cordova: {
        options: {
          command: ['platform', 'plugin', 'build'],
          platforms: ['ios', 'android'],
          plugins: ['device', 'dialogs'],
          path: '../cordova/www',
          id: 'io.cordova.hellocordova',
          name: 'HelloCordova'
        }
      },
//      add_platforms: {
//        options: {
//          command: 'platform',
//          action: 'add',
//          platforms: ['ios', 'android']
//        }
//      },
      add_plugins: {
        options: {
          command: 'plugin',
          action: 'add',
          plugins: [
//            'battery-status',
//            'camera'
//            'console',
//            'contacts',
//            'device',
//            'device-motion',
//            'device-orientation',
//            'dialogs',
//            'file',
//            'geolocation',
//            'globalization',
//            'inappbrowser',
//            'media',
//            'media-capture',
//            'network-information',
//            'splashscreen',
//            'vibration'
          ]
        }
      },
      build_ios: {
        options: {
          command: 'build',
          platforms: ['ios']
        }
      },
      build_android: {
        options: {
          command: 'build',
          platforms: ['android']
        }
      },
      emulate_android: {
        options: {
          command: 'emulate',
          platforms: ['android'],
          args: ['--target', 'Nexus5']
        }
      }
    }


  });

  // Tasks
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-csslint');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-ng-annotate');
  grunt.loadNpmTasks('grunt-html-angular-validate');
  grunt.loadNpmTasks('grunt-ng-constant');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-usemin');
  grunt.loadNpmTasks('grunt-filerev');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-cordovacli');

  grunt.registerTask('app', [
    'copy:app'
  ]);

  grunt.registerTask('www', [
    'copy:www'
  ]);

  // Default task(s).
  grunt.registerTask('default', [
    'clean:build',
    'ngconstant:development',
    'csslint',
    'useminPrepare',
    'concat:generated',
    'cssmin:generated',
    'ngAnnotate:generated',
    'uglify',
    'copy:generated',
//    'filerev',
    'usemin'
  ]);

  grunt.registerTask('prod', [
    'clean:build',
    'ngconstant:production',
    'csslint',
    'useminPrepare',
    'concat:generated',
    'cssmin:generated',
    'ngAnnotate:generated',
    'uglify',
    'copy:generated',
//    'filerev',
    'usemin'
  ]);

};
