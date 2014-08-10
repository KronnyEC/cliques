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
        templateUrl: 'templates/post_detail.html',
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
  .config(function ($sceDelegateProvider) {
    $sceDelegateProvider.resourceUrlWhitelist([
      'self',
      'http://**.youtube.com/**'
    ]);
  })
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
    };
    this.destroy = function () {
      this.id = null;
      this.username = null;
      token = null;
    };
    return this;
  })
  .factory('Notification', function ($http, $rootScope, $timeout, BACKEND_SERVER) {
    var Notifications = {};
    Notifications.notifications = [];

    Notifications.remove_all = function () {
      for (var i = 0; i < Notifications.notifications.length; i++) {
        var item = Notifications.notifications[i];
        $http.delete(BACKEND_SERVER + 'notifications/' + item.id + '\/');
      }
      Notifications.notifications.splice(0, Notifications.notifications.length + 1);
    };

    Notifications.remove_notification = function (item) {
      console.log("notification remove", item);
      $http.delete(BACKEND_SERVER + 'notifications/' + item.id + '\/')
        .success(function (res) {
          console.log('removed notification', item.id);
          for (var i = 0; i < Notifications.notifications.length; i++) {
            if (Notifications.notifications[i].id == item.id) {
              Notifications.notifications.splice(i, 1);
              break;
            }
          }
        });
    };

    // Get the first page of results
    $http.get(BACKEND_SERVER + 'notifications\/').success(function (results) {
      console.log('note results', results);
      results.results.forEach(function (n) {
        Notifications.notifications.push(n);
      });
    });

    // Listen to Channel updates for notifications
    $rootScope.$on('notification', function (event, message) {
      Notifications.notifications.push(message);
    });

    // Listen for location changes, remove notifications if user sees page that
    // they were notified about changes on
    $rootScope.$on('$routeUpdate', function () {
      console.log('remove notifications')
    });

    return Notifications
  })
  .factory('User', function ($http, $interval, $rootScope, BACKEND_SERVER) {
    var Users = {};
    Users.users = [];
    Users.connected_users = [];

    function set_connected_users() {
      var now = new Date();
      // 60 seconds
      var disconnect_threshold = 1000 * 60;
      Users.connected_users = [];
      Users.users.forEach(function (user) {
        console.log('connected user?', user, now, now - Date.parse(user.last_updated));
        if ((now - Date.parse(user.last_updated)) < disconnect_threshold) {
          console.log('user is connected', user);
          Users.connected_users.push(user);
        }
      });
      $rootScope.$apply();
      console.log('Users.connected_users', Users.connected_users);
    }

    var get_users = function () {
      $http.get(BACKEND_SERVER + 'users/').success(function (result) {
        console.log('users list', result);
        Users.users = [];
        result.results.forEach(function (user) {
          Users.users.push(user);
        });
        console.log('users.users', Users.users);
        set_connected_users();
      })
    };

    // Check in every 15 seconds.
    var check_in = function () {
      $http.post(BACKEND_SERVER + 'check_in\/', {}).success(function (result) {
        console.log('checked in', result);
//        Users.connected_users = [];
        get_users();

      });
    };

    var stop = $interval(function() {
      console.log('interval');
      check_in()
    }, 15 * 1000);

    check_in();
    console.log('connected', Users);
    return Users;
  })
  .factory('Chat', function ($http, $rootScope, $interval, Channel, BACKEND_SERVER) {
    var Chats = {};
    Chats.messages = [];
    Chats.messages = Channel.stream;
    Chats.connected_users = [];
    Chats.session = Channel.session;
    console.log('Chat init', Chats);
    var session_data = {
      'id': Chats.session.id
    };

    // Get the first page of results
    $http.get(BACKEND_SERVER + 'chat/messages\/').success(function (results) {
      console.log('messages results', results);
      results.results.reverse().forEach(function (message) {
        Chats.messages.push(message);

      });
    });

    $rootScope.$on('chat', function (event, message) {
      Chats.messages.push(message);
    });

    return Chats;
  })
  .factory('Channel', function ($rootScope, $http, BACKEND_SERVER) {
    var Notifications = {};
    Notifications.stream = [];
    Notifications.session = {};

    var messageCallback = function (data) {
      // Call back on every Channel message. Broadcast out with type to
      // listeners
      data = angular.fromJson(data.data);
      $rootScope.$apply(function () {
        console.log('message callback', data.type, data.data);
        if (data) {
          console.log('broadcast', data.type, data.data);
          $rootScope.$broadcast(data.type, data.data);
        }
      })
    };

    var SocketHandler = function (BACKEND_SERVER, session, onMessageCallback) {
      var context = this;
      this.socketCreationCallback = function (token) {
        console.log('token', token);
        var channel = new goog.appengine.Channel(token);
        context.channelId = channel.channelId;

        var socket = channel.open();
        socket.onerror = function (e) {
          console.log("Channel error", e);
        };
        socket.onclose = function () {
          console.log("Channel closed");
        };
        socket.onmessage = messageCallback;

        context.channelSocket = socket;
      };
      this.socketCreationCallback(session.session_key);
    };

    // init
    Notifications.session = $http.post(BACKEND_SERVER + 'push\/', {})
      .success(function (result) {
        console.log('new session created', result);
        return result;
      });

    //that's where we connect
    Notifications.session.then(function (s) {
      var socket = new SocketHandler(BACKEND_SERVER, s.data, messageCallback);
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

app.run(function (Notification) {
});

app.run(function (User) {
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

function highlight(text, highlight_text) {
  text = text.insert(text.indexOf(highlight_text) - 1, '<span class="highlight">');
  return text.insert(text.indexOf(highlight_text) + highlight_text.length, '</span>');

}

// Add insert so we can add highlights easily.
String.prototype.insert = function (index, string) {
  if (index > 0)
    return this.substring(0, index) + string + this.substring(index, this.length);
  else
    return string + this;
};