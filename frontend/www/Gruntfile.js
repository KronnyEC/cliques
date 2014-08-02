module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      build: {
        src: 'src/<%= pkg.name %>.js',
        dest: 'build/<%= pkg.name %>.min.js'
      }
    },
    csslint: {
      options: {
        force: true,
        absoluteFilePathsForFormatters: true,
      },
      lax: {
        options: {
          import: false
        },
        src: ['css/*.css']
      }
    }
  });

  // Tasks
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-csslint');

  // Default task(s).
  grunt.registerTask('default', ['uglify', 'csslint']);

};
