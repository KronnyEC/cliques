var app = angular.module('cliques', [
    'ngCookies',
    'ngResource',
    'ngRoute',
//    'ngSanitize',
    'post_controllers'
]);

app.config(['$routeProvider',
    function($routeProvider, $httpProvider, $cookies) {
//      $httpProvider.responseInterceptors.push('httpInterceptor');
//      $locationProvider.html5Mode(true);
        $routeProvider.
            when('/posts', {
                templateUrl: 'templates/posts.html',
                controller: 'PostListCtrl'
            }).
            when('/posts/:id', {
                templateUrl: 'templates/post.html',
                controller: 'PostDetailCtrl'
            }).
            when('/new_post/', {
                templateUrl: 'templates/new_post.html',
                controller: 'NewPostCtrl'
            }).
            when('/login', {
                templateUrl: 'templates/login.html',
                controller: 'AuthCtrl'
            }).
            otherwise({
                redirectTo: '/posts'
            });
    }

])
.config(['$httpProvider', function($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }
])
.service('Session', function () {
  this.create = function (sessionId, userId, token) {
    this.id = sessionId;
    this.username = username;
    this.token = token;
  };
  this.destroy = function () {
    this.id = null;
    this.username = null;
    this.token = null;
  };
  return this;
})
.constant('USER_ROLES', {
  all: '*',
  admin: 'admin',
  editor: 'editor',
  guest: 'guest'
})
.constant('AUTH_EVENTS', {
  loginSuccess: 'auth-login-success',
  loginFailed: 'auth-login-failed',
  logoutSuccess: 'auth-logout-success',
  sessionTimeout: 'auth-session-timeout',
  notAuthenticated: 'auth-not-authenticated',
  notAuthorized: 'auth-not-authorized'
})
.constant('angularMomentConfig', {
    preprocess: 'unix', // optional
    timezone: 'America/Chicago' // optional
});

app.run(function($cookieStore, $rootScope, $http) {
  	if ($cookieStore.get('djangotoken')) {
      $http.defaults.headers.common['Authorization'] = 'Token ' + $cookieStore.get('djangotoken');
//      document.getElementById("main").style.display = "block";
    } else {
//    	document.getElementById("login-holder").style.display = "block";
    }
});