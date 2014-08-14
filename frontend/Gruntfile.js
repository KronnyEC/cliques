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
          dest: 'build/js/cliques_config.js'
        },
        constants: {
          ENV: 'development',
          BACKEND_SERVER: 'http://127.0.0.1:8080/api/v1/'
        }
      },
      production: {
        options: {
          dest: 'build/js/cliques_config.js'
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
            src: ['spec/'],
            dest: 'build/'
          },
          {
            expand: true,
            src: ['res/'],
            dest: 'build/'
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
            src: ['build/js/*'],
            dest: '../www/js/'
          },
          {
            src: ['build/css/*'],
            dest: '../www/css/'
          },
          {
            src: ['build/partials/*'],
            dest: '../www/partials/'
          },
          {
            src: ['build/templates/*'],
            dest: '../www/templates/'
          },
          {
            src: ['build/partials/*'],
            dest: '../www/partials/'
          },
          {
            src: ['build/index.html'],
            dest: '../www/index.html'
          }
        ]
      },
      app: {
        files: []
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

};
