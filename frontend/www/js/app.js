var app = angular.module('cliques', [
  'ngCookies',
  'ngResource',
  'ngRoute',
//    'ngSanitize',
  'infinite-scroll',
  'mm.foundation',
  'post_controllers'
]);

app.config(['$routeProvider',
  function ($routeProvider, $httpProvider, $cookies) {
//      $httpProvider.responseInterceptors.push('httpInterceptor');
//      $locationProvider.html5Mode(true);
    $routeProvider.

      when('/posts', {
        templateUrl: 'templates/posts.html',
        controller: 'PostListCtrl'
      }).
      when('/posts/:postId', {
        templateUrl: 'templates/post.html',
        controller: 'PostDetailCtrl'
      }).
      when('/new_post', {
        templateUrl: 'templates/new_post.html',
        controller: 'NewPostCtrl'
      }).
      when('/login', {
        templateUrl: 'templates/login.html',
        controller: 'AuthCtrl'
      }).
      when('/chat', {
        templateUrl: 'templates/chat.html',
        controller: 'ChatCtrl'
      }).
      when('/users/:username', {
        templateUrl: 'templates/profile.html',
        controller: 'UserCtrl'
      }).
      when('/polls', {
        templateUrl: 'templates/polls.html',
        controller: 'PollListCtrl'
      }).
      when('/polls/:pollStub', {
        templateUrl: 'templates/poll.html',
        controller: 'PollDetailCtrl'
      }).
      when('/notifications', {
        templateUrl: 'templates/notifications.html',
        controller: 'NotificationCtrl'
      }).
//            when('/invite', {
//                templateUrl: 'templates/invite.html',
//                controller: 'InviteCtrl'
//            }).
      otherwise({
        redirectTo: '/posts'
      });
  }

])
  .config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  }])
  .constant("BACKEND_SERVER", "http://127.0.0.1:8080/api/v1/")
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
  })
  .service('Session', function () {
    this.create = function (sessionId, userId, token) {
      this.id = sessionId;
      this.username = username;
      token = token;
    };
    this.destroy = function () {
      this.id = null;
      this.username = null;
      token = null;
    };
    return this;
  })
  .factory('Notifications', function ($http, $timeout, BACKEND_SERVER) {
    var data = [];
    var poller = function () {
      $http.get(BACKEND_SERVER + 'notifications\/').then(function (r) {
        data = r.data.results;
        $timeout(poller, 30000);
      });
    };
    poller();

    return {
      data: data
    };
  })
  .factory('Chat', function ($http, $timeout, BACKEND_SERVER) {
    var token;
    var chan;
    var socket;
    var messages = [];
    var connected_users = [];
    var session;

    function get_messages() {
      // callback will get a list of messages as the only arg
      console.log(BACKEND_SERVER + 'chat/messages\/');
      $http.get(BACKEND_SERVER + 'chat/messages\/')
        .then(function (results) {
          console.log('get messages', results);
          messages = results.data.results;
          console.log('got messages', messages);
        })
    }

    function check_in(callback) {
      console.log('check in');
      $http.post(BACKEND_SERVER + 'chat/check_in\/', {})
        .success(function (result) {
          connected_users = result.connected_users;
        });
    }

    function leave_chat() {
      // not yet called
      $http.post(BACKEND_SERVER + 'chat/leave_chat\/')
        .success(function (result) {
          console.log("left chat", result);
        });
    }

    function socket_open(e) {
      console.log("Socket opened");
    }

    function socket_error(e) {
      var code = e.field;
      var description = e.description;
      console.log("Socket error", code, description);
      // Token timed out, get a new one.
      if (code == 401 && description == "Token+timed+out.") {
        join_chat();
      }
    }

    function socket_close(e) {
      console.log("Socket closed", e);
    }

    function build_socket() {
      console.log('building socket', token);
      chan = new goog.appengine.Channel(token);
      console.log('tokenchan', token, chan);
      socket = chan.open({
        onerror: function (e) {
          console.log('socket error: ', e);
        },
        onmessage: function (e) {
          console.log('socket message', e);
          messages.push(e)
        },
        onopen: function (e) {
          console.log("Socket opened", e);
        },
        onclose: function (e) {
          console.log("Socket closed", e);
        }
      });
      console.log("Socket", chan, socket)
    }

    function join_chat() {
      console.log('join chat', BACKEND_SERVER + 'chat/sessions\/');
      if (token != undefined) {

      } else {
        $http.post(BACKEND_SERVER + 'chat/sessions\/', {})
          .success(function (result) {
            console.log("session result", result);
            session = result;
            token = result.session_key;
            build_socket();
          });
      }
    }

    console.log('joining chat');
    join_chat();
    console.log('chat joined');
    get_messages();
    console.log('init messages', messages, connected_users);
    return {
      messages: $http.get(BACKEND_SERVER + 'chat/messages\/'),
      connected_users: connected_users,
      session: session
    }
  });

app.run(function ($rootScope, $http, $location) {
  angular.module('infinite-scroll').value('THROTTLE_MILLISECONDS', 250);
  if (localStorage.getItem('token')) {
    $http.defaults.headers.common['Authorization'] = 'Token ' + localStorage.getItem('token');
    $rootScope.loggedIn = true;
  } else {
    $rootScope.loggedIn = false;
  }
  $rootScope.$watch(function () {
    return $location.path();
  }, function (newValue, oldValue) {
    if ($rootScope.loggedIn == false && newValue != '/login') {
      $location.path('/login');
    }
  });
});

app.run(function (Notifications) {
});

function urlify(text) {
  var expression = /(^|\s)((https?:\/\/)?[\w-]+(\.[\w-]+)+\.?(:\d+)?(\/\S*)?)/gi;

  var regex = new RegExp(expression);
  var t = 'www.google.com';
  return text.replace(regex, function (url) {
    return '<a href="' + url + '">' + url + '</a>';
  });
  // or alternatively
  // return text.replace(urlRegex, '<a href="$1">$1</a>')
}