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

    return {
      data: data
    };
  })
  .factory('Chat', function($http, Channel, BACKEND_SERVER) {
    var Chats = {};
    Chats.messages = [];
    Chats.messages = Channel.stream;
    Chats.connected_users = [];
    Chats.session = Channel.session;
    console.log('Chat init', Chats);

    $http.get(BACKEND_SERVER + 'chat/messages\/').success(function(results) {
      console.log('messages results', results)
      results.results.forEach(function(message) {
        Chats.messages.push(message);
      });
    })
    return Chats;
  })
  .factory('Channel', function ($rootScope, $http, BACKEND_SERVER) {
    var Notifications = {};
    Notifications.stream = [];
    Notifications.session = {};

    // Broadcast changes in notifications
//    $rootScope.$watch(Notifications.stream, function(notification) {
//      console.log('broadcasting', notification);
//      if (notification) {
//        $rootScope.$broadcast(notification.type, notification.data);
//      }
//    });

    var SocketHandler = function (BACKEND_SERVER, session, $rootScope) {
      console.log('creating socket handler for ', BACKEND_SERVER, session);
      this.messageCallback = function () {
      };

      var context = this;
      this.socketCreationCallback = function (token) {
        console.log('socket created', token);
        var channel = new goog.appengine.Channel(token);
        console.log('channel', channel);
        context.channelId = channel.channelId;
        var socket = channel.open();
        socket.onerror = function () {
          console.log("Channel error");
        };
        socket.onclose = function () {
          console.log("Channel closed");
        };
        socket.onmessage = function(message) {
          console.log('message received', message)
          var data = JSON.parse(message.data);
//          console.log('broadcasting', data);
          Notifications.stream.push(data);
//          console.log('notes', Notifications);
        };
        context.channelSocket = socket;
      };
      console.log('sending root scope');
      this.socketCreationCallback(session.session_key);
      var post_data = {
        'session': session.id,
        'message': 'test'
      };
      console.log('post_data', post_data);
    };

    // init
    Notifications.session = $http.post(BACKEND_SERVER + 'chat/sessions\/', {})
      .success(function (result) {

        console.log('notification', result);
        return result;
      });

    //that's where we connect
      Notifications.session.then(function(s) {
      console.log('socket building', s.data);
      var socket = new SocketHandler(BACKEND_SERVER, s.data);
      console.log('built socket', socket);
    });

    return Notifications;
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