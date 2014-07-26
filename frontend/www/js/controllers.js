angular.module('post_controllers', [])
  .controller('UserCtrl', function ($scope, $rootScope, $http, BACKEND_SERVER) {
    // Get data on startup
    var username = localStorage.getItem('username');
    $http.get(BACKEND_SERVER + 'users/' + username + '\/')
      .then(function (res) {
        console.log('user result', res);
        $scope.user = res.data
      });

  })
  .controller('PostListCtrl', function ($scope, $http, $sce, BACKEND_SERVER) {
    // Get data on startup
    $http.get(BACKEND_SERVER + 'posts/')
      .then(function (res) {
        $scope.posts = res.data.results;
        console.log($scope.posts);
      });
    $scope.infiniteScroll = function () {
      console.log('scroll!');
    };
    $scope.trustSrc = function(src) {
      return $sce.trustAsResourceUrl(src);
    };
    console.log("post list auth", $http.defaults.headers.common.Authorization)
  })
  .directive('media', function () {

    return {
      restrict: 'AE',
      transclude: true,
      replace: false,
      templateUrl: 'templates/media.html'
    }
  })
  .controller('PostDetailCtrl', function ($scope, $http, $routeParams, $location, BACKEND_SERVER) {
    $scope.postId = $routeParams.postId;
    $http.get(BACKEND_SERVER + 'posts/' + $scope.postId + '\/')
      .then(function (res) {
        $scope.post = res.data;
      });
    $scope.new_comment_submit = function () {
      $scope.formData['post'] = $scope.postId;
      console.log("submitting", $scope.formData, this);
      $http({
        url: BACKEND_SERVER + 'posts\/' + $scope.postId + '/comments\/',
        method: "POST",
        data: $.param($scope.formData),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Authorization': 'Token ' + localStorage.getItem('token')
        }
      }).success(function (data, status, headers, config) {
        console.log('new post');
        $location.path('/#/posts/' + $scope.postId);
      }).error(function ($scope, data, status, headers, config) {
        console.log('error', data);
        $scope.status = status + ' ' + headers;
      });
    };
  })
  .controller('AuthCtrl', function ($scope, $rootScope, $location, httpInterceptor, authorization, api, AuthService, Auth) {
    $scope.credentials = {
      username: '',
      password: ''
    };
    $scope.login = function (credentials) {
      Auth.setCredentials($rootScope, credentials);
      $location.path('/#/posts');
    };
  })
  .filter('DTSince', function () {
    return function (dt) {
      var now = new Date();
      var difference = (now - Date.parse(dt)) / 1000;
      if (difference < 10) {
        return "A few seconds ago"
      }
      else if (difference < 60) {
        return Math.floor(difference) + " seconds ago";
      }
      else if (difference < 3600) {
        return Math.floor(difference / 60) + " minutes ago";
      }
      else if (difference < 86400) {
        return Math.floor(difference / 3600) + " hours ago";
      }
      else if (difference < 2592000) {
        return Math.floor(difference / 86400) + " days ago";
      }
      else if (difference < 77760000) {
        return Math.floor(difference / 2592000) + " months ago";
      }
      else if (difference < 933120000) {
        return Math.floor(difference / 77760000) + " years ago";
      }
      else if (difference < 9331200000) {
        // :) A guy can dream, right?
        // Hope there's no leap seconds..
        return Math.floor(difference / 933120000) + " decades ago";
      }

    }
  })
  .factory('httpInterceptor', function httpInterceptor($q, $window, $location) {
    return function (promise) {
      console.log('http intercepted');
      var success = function (response) {
        return response;
      };

      var error = function (response) {
        if (response.status === 401) {
          $location.path('/login');
        }

        return $q.reject(response);
      };

      return promise.then(success, error);
    };
  })

  .factory('authorization', function ($http) {
    var url = 'http://127.0.0.1:8080';

    return {
      login: function (credentials) {
        return $http.post(url + '/api/token\/', credentials);
      }
    };
  })

  .factory('api', function ($http, $cookies) {
    return {
      init: function (token) {
        $http.defaults.headers.common['X-Access-Token'] = token || $cookies.token;
      }
    };
  })
  .factory('AuthService', function ($http, $cookies, Session) {
    return {
      login: function (credentials) {
        // Get the CSRF token :(
        return $http.get('http://127.0.0.1:8080/api/cookie\/').then(
          $http
            .post('http://127.0.0.1:8080/auth/login\/', credentials)
            .then(function (res) {
              Session.create(res.id, res.username, res.token);
            }));
      },
      isAuthenticated: function () {
        return !!Session.userId;
      }
    };
  })
  .factory('Auth', ['Base64', '$http', '$rootScope', '$location', function (Base64, $http, $location, BACKEND_SERVER) {
    // initialize to whatever is in the cookie, if anything
    $http.defaults.headers.common['Authorization'] = 'Token ' + localStorage.getItem('token');

    return {
      setCredentials: function (scope, credentials) {
        var encoded = Base64.encode(credentials['username'] + ':' + credentials['password']);
        console.log('encoded', encoded);
        $http({
          url: BACKEND_SERVER + 'token\/',
          method: "GET",
          headers: {
            'Authorization': 'Basic ' + encoded
          }
        }).success(function (data, status, headers, config) {
          console.log('data', data);
          var token = data['token'];
          $http.defaults.headers.common.Authorization = 'Token ' + token;
          localStorage.setItem('token', token);
          localStorage.setItem('username', data['username']);
          scope.loggedIn = true;
          $location.path('/#/posts');
        }).error(function (data, status, headers, config) {
          console.log('login error', status, headers);
        });
      },
      clearCredentials: function () {
        document.execCommand("ClearAuthenticationCache");
        localStorage.removeItem('token');
        $http.defaults.headers.common.Authorization = 'Basic ';
        $rootScope.loggedIn = false;
      }
    };
  }])
  .factory('Base64', function () {
    var keyStr = 'ABCDEFGHIJKLMNOP' +
      'QRSTUVWXYZabcdef' +
      'ghijklmnopqrstuv' +
      'wxyz0123456789+/' +
      '=';
    return {
      encode: function (input) {
        var output = "";
        var chr1, chr2, chr3 = "";
        var enc1, enc2, enc3, enc4 = "";
        var i = 0;

        do {
          chr1 = input.charCodeAt(i++);
          chr2 = input.charCodeAt(i++);
          chr3 = input.charCodeAt(i++);

          enc1 = chr1 >> 2;
          enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
          enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
          enc4 = chr3 & 63;

          if (isNaN(chr2)) {
            enc3 = enc4 = 64;
          } else if (isNaN(chr3)) {
            enc4 = 64;
          }

          output = output +
            keyStr.charAt(enc1) +
            keyStr.charAt(enc2) +
            keyStr.charAt(enc3) +
            keyStr.charAt(enc4);
          chr1 = chr2 = chr3 = "";
          enc1 = enc2 = enc3 = enc4 = "";
        } while (i < input.length);

        return output;
      },

      decode: function (input) {
        var output = "";
        var chr1, chr2, chr3 = "";
        var enc1, enc2, enc3, enc4 = "";
        var i = 0;

        // remove all characters that are not A-Z, a-z, 0-9, +, /, or =
        var base64test = /[^A-Za-z0-9\+\/\=]/g;
        if (base64test.exec(input)) {
          alert("There were invalid base64 characters in the input text.\n" +
            "Valid base64 characters are A-Z, a-z, 0-9, '+', '/',and '='\n" +
            "Expect errors in decoding.");
        }
        input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

        do {
          enc1 = keyStr.indexOf(input.charAt(i++));
          enc2 = keyStr.indexOf(input.charAt(i++));
          enc3 = keyStr.indexOf(input.charAt(i++));
          enc4 = keyStr.indexOf(input.charAt(i++));

          chr1 = (enc1 << 2) | (enc2 >> 4);
          chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
          chr3 = ((enc3 & 3) << 6) | enc4;

          output = output + String.fromCharCode(chr1);

          if (enc3 != 64) {
            output = output + String.fromCharCode(chr2);
          }
          if (enc4 != 64) {
            output = output + String.fromCharCode(chr3);
          }

          chr1 = chr2 = chr3 = "";
          enc1 = enc2 = enc3 = enc4 = "";

        } while (i < input.length);

        return output;
      }
    };
  })
  .controller('NewPostCtrl', function ($scope, $rootScope, $http, $location, BACKEND_SERVER) {
    // Get a list of categories for the dropdown
    $http.get(BACKEND_SERVER + 'categories/')
      .success(function (res, status, headers, config) {
        console.log('categories', res);
        $scope.cats = res;
      });

    $scope.formData = {};

    $scope.new_post_submit = function () {
      console.log("submitting", $scope.formData);
      $http({
        url: BACKEND_SERVER + 'posts\/',
        method: "POST",
        data: $.param($scope.formData),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Authorization': 'Token ' + localStorage.getItem('token')
        }
      }).success(function (data, status, headers, config) {
        console.log('new post');
        $location.path('/#/posts')
      }).error(function ($scope, data, status, headers, config) {
        console.log('error', data);
        $scope.status = status + ' ' + headers;
      });
    };

  })
  .controller('ProfileCtrl', function () {

  })
  .controller('ChatCtrl', function ($scope, $http, Chat, BACKEND_SERVER) {
    $scope.messages = [];

    $scope.messages = Chat.messages;
    $scope.connected_users = Chat.connected_users;
    console.log('connected_users', $scope.connected_users)
    Chat.session.success(function (result) {
      $scope.session = result;
    });

    $scope.send_message = function () {
      console.log($scope.text, $scope.session);
      $http({
        method: 'POST',
        url: BACKEND_SERVER + 'chat/messages\/',
        data: {'message': $scope.text}
      });
      $scope.text = "";
    };
  })
  .filter('UsernameFilter', function () {
    return function (userid) {
      var users = {1: 'josh'};
      return users[userid]
    }
  })
  .filter('ChatMessageFilter', function () {
    return function (message) {
      return message.replace('\n', '<br/>')
    }
  })
  .directive('ngEnter', function () {
    return function (scope, element, attrs) {
      element.bind("keydown keypress", function (event) {
        if (event.which === 13) {
          scope.$apply(function () {
            scope.$eval(attrs.ngEnter, {'event': event});
          });

          event.preventDefault();
        }
      });
    };
  })
  .controller('PollListCtrl', function (BACKEND_SERVER) {
    $http.get(BACKEND_SERVER + 'polls\/')
      .then(function (res) {
        $scope.polls = res.data.results;
      });
  })
  .controller('PollDetailCtrl', function ($scope, $http, $routeParams, $location, BACKEND_SERVER) {
    $scope.pollStub = $routeParams.pollStub;
    console.log('/#/polls/' + $scope.pollStub);
    $scope.new_submission_submit = function () {
      $scope.formData['poll'] = $scope.poll.id;
      console.log("submitting", $scope.formData, this, $scope.poll);
      $http({
        url: BACKEND_SERVER + 'polls\/' + $scope.pollStub + '/submissions\/',
        method: "POST",
        data: $.param($scope.formData),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Authorization': 'Token ' + localStorage.getItem('token')
        }
      }).success(function (data, status, headers, config) {
        console.log('new post');
        $location.path('/#/polls/' + $scope.pollStub);
      }).error(function ($scope, data, status, headers, config) {
        console.log('error', data);
        $scope.status = status + ' ' + headers;
      });
    };
    $scope.removeVote = function (id) {
      console.log('removeVote');
      $http({
        url: BACKEND_SERVER + 'votes/' + id + '\/',
        method: "DELETE",
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Authorization': 'Token ' + localStorage.getItem('token')
        }
      }).success(function (data, status, headers, config) {
        console.log('vote killed', data);
      }).error(function ($scope, data, status, headers, config) {
        console.log('error', data);
      })
    };
    $scope.addVote = function (id) {
      console.log('addVote');
      var data = {'submission': id, 'user': $scope.user.id};
      console.log('submitting', data);
      $http({
        url: BACKEND_SERVER + 'votes\/',
        method: "POST",
        data: $.param(data),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Authorization': 'Token ' + localStorage.getItem('token')
        }
      }).success(function (data, status, headers, config) {
        consol.log('new vote', data);
      }).error(function ($scope, data, status, headers, config) {
        console.log('error', data);
      })
    };

    $http.get(BACKEND_SERVER + 'polls/' + $scope.pollStub + '\/')
      .then(function (res) {
        console.log('poll results', res);
        $scope.poll = res.data;
      });
  })
  .controller('InviteCtrl', function () {
    $scope.invite_submit = function () {
      console.log("submitting", $scope.formData, $rootScope.basic_authorization);
      $http({
        url: BACKEND_SERVER + 'invite\/',
        method: "POST",
        data: $.param($scope.formData),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Authorization': 'Token ' + localStorage.getItem('token')
        }
      }).success(function ($location, data, status, headers, config) {
        $location.path('/#/posts')
      }).error(function ($scope, data, status, headers, config) {
        console.log('error', data);
        $scope.status = status + ' ' + headers;
      });
    }
  })
  .controller('NotificationCtrl', function ($scope, $http, Notifications, BACKEND_SERVER) {
    console.log('notectrl');
    $scope.remove_all = function () {
      $http.delete(BACKEND_SERVER + 'notifications\/')
        .success(function (res) {
          console.log('removed all notifications')
        });
    };
    $scope.remove_notification = function (location) {
      console.log("notification remove", item);
      $http.delete(BACKEND_SERVER + 'notifications/' + item.id + '\/')
        .success(function (res) {
          console.log('removed notification', item.id);
        });
    };
    console.log("notedata", Notifications);
    $scope.notifications = Notifications;
  })
  .controller('TabCtrl', function ($scope, Channel) {
    $scope.chat_count = Channel.stream.length;
    $scope.tabs = [
      {'name': 'Posts', 'link': '/#/posts', 'alert': ''},
      {'name': 'Notifications', 'link': '/#/notifications', 'alert': ''},
      {'name': 'Chat', 'link': '/#/chat', 'alert': $scope.chat_count},
      {'name': 'BotD', 'link': '/#/polls/BotD', 'alert': ''},
      {'name': 'Profile', 'link': '/#/profile', 'alert': ''}
    ];
    $scope.selected = $scope.tabs[0];
    $scope.select = function (item) {
      $scope.selected = item;
    };
    $scope.itemClass = function (item) {
      return item === $scope.selected ? 'active' : undefined;
    };
  })
  .controller('OffCanvasDemoCtrl', function ($scope) {
  });

function removeChatIfAlreadyExists(chat, array) {
  var result = array.filter(function (potentialMatch) {
    return potentialMatch.id != chat.id;
  });

  return result;
}

