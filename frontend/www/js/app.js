var app = angular.module('cliques', [
    'ngCookies',
    'ngResource',
    'ngRoute',
//    'ngSanitize',
    'infinite-scroll',
    'mm.foundation',
    'post_controllers'
]);

var backend_server = 'http://127.0.0.1:8080/api/v1';

app.config(['$routeProvider',
    function($routeProvider, $httpProvider, $cookies) {
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
.service('NotificationService', function($http, $interval) {
    var service = {

    }
    return service;
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

app.run(function($rootScope, $http, $location) {
    angular.module('infinite-scroll').value('THROTTLE_MILLISECONDS', 250);
  	if (localStorage.getItem('token')) {
        $http.defaults.headers.common['Authorization'] = 'Token ' + localStorage.getItem('token');
        $rootScope.loggedIn = true;
    } else {
        $rootScope.loggedIn = false;
    }
    $rootScope.$watch(function() { return $location.path(); }, function(newValue, oldValue){
        if ($rootScope.loggedIn == false && newValue != '/login'){
                $location.path('/login');
        }
    });
});

app.service('chatService', function($http) {
    var chat_server = 'http://www.slashertraxx.com/';
    var token;
    return {
        socket_open: function(e) {
            console.log("Socket opened");
        },

        socket_error: function(e) {
            var code = e.field;
            var description = e.description;
            console.log("Socket error", code, description);
            // Token timed out, get a new one.
            if (code == 401 && description == "Token+timed+out.") {
                this.join_chat();
            }
        },

        socket_close: function(e) {
            console.log("Socket closed", e);
        },

        build_socket: function(on_message_callback) {
            console.log('building socket', this.token);

            this.chan = new goog.appengine.Channel(this.token);
            goog.appengine.Socket.BASE_URL = "http://localhost:8080" + goog.appengine.Socket.BASE_URL;
            console.log('tokenchan', this.token, this.chan);
            console.log('error', this);
            this.socket = this.chan.open({
                onerror: function(e) {
                    console.log('socket error: ', e)
                },
                onmessage: on_message_callback,
                onopen: function(e) {
                    console.log("Socket opened", e);
                },
                onclose: function(e) {
                    console.log("Socket closed", e);
                }
            });
        },

        join_chat: function(on_message_callback) {
            console.log('join chat', backend_server + '/chat/sessions/');
            var build_socket = this.build_socket;
            if (this.token != undefined) {

            } else {
                $http.post(backend_server + '/chat/sessions/', {})
                .success(function (result) {
                    console.log("result", result);
                    this.token = result.session_key;
                    console.log(this.token, this.build_socket, on_message_callback)
                    build_socket(on_message_callback);
                });
            }
        },

        get_messages: function(callback) {
            // callback will get a list of messages as the only arg
            $http.get({
                url: backend_server + '/chat/messages/'
            }).success(function (results) {
                callback(results)
            })
        },

        send_message: function(msg) {
            console.log(this.socket, msg);
            $http.post({
                url: backend_server + '/chat/message/',
                data: {'msg': msg}
            });
        },

        check_in: function(callback) {
            console.log('check in');
            $http.post(backend_server + '/chat/check_in/', {})
                .success(function (result) {
                    callback(result.connected_users);
                });
        },

        leave_chat: function() {
            $.http.post({
                url: backend_server + '/chat/leave_chat/'
            }).success(function (result) {
                console.log("left chat", result);
            });
        }
    }
});

function urlify(text) {
    var expression = /(^|\s)((https?:\/\/)?[\w-]+(\.[\w-]+)+\.?(:\d+)?(\/\S*)?)/gi;

    var regex = new RegExp(expression);
    var t = 'www.google.com';
    return text.replace(regex, function(url) {
        return '<a href="' + url + '">' + url + '</a>';
    });
    // or alternatively
    // return text.replace(urlRegex, '<a href="$1">$1</a>')
}