module.exports = function(grunt) {

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
            'js/controllers.js',
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
      },
      combine: {
        files: {
          'build/cliques.min.css': [

            'bower_components/foundation/css/foundation.css',
            'bower_components/foundation/css/normalize.css',
            'css/cliques.css'
          ]
        }
      }
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
   }
  });

  // Tasks
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-csslint');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-ngmin');
  grunt.loadNpmTasks('grunt-html-angular-validate');


  // Default task(s).
  grunt.registerTask('default', ['csslint', 'cssmin', 'ngmin']);

};
