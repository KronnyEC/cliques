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
  .controller('UsersCtrl', function ($scope, $interval, $http, BACKEND_SERVER, User) {
    $scope.$watch(function() {
      $scope.users = User.users;
      $scope.connected_users = User.connected_users;
    })

  })
  .controller('PostListCtrl', function ($scope, $http, $sce, BACKEND_SERVER) {
    // Get data on startup
    var page = 1;
    var busy = false;
    $scope.posts = [];
    var add_pages = function(post_page) {
//      console.log('add pages', post_page);
      busy = true;
      if (post_page == undefined) {
        post_page = 1;
      }
      $http.get(BACKEND_SERVER + 'posts/?page=' + post_page)
      .then(function (res) {
        res.data.results.forEach(function (result) {
          result.youtube = youtube_url_to_id(result.url);
          result.nsfw_show = false;
          $scope.posts.push(result);
        });
//        console.log($scope.posts);
        page = post_page;
        busy = false;
//        $scope.$apply();
      });
    };

    $scope.scroll = function () {
      if (busy) {
        console.log('attempted scroll');
        return;
      }
      add_pages(page + 1);
      console.log('scroll!');
    };

    $scope.toggleNSFW = function(post) {
      post.nsfw_show = !post.nsfw_show;
    };

    $scope.trustSrc = function (src) {
      return $sce.trustAsResourceUrl(src);
    };

    // Add first round of pages
    add_pages(1);
//    console.log("post list auth", $http.defaults.headers.common.Authorization)
  })

  .directive('media', function () {
    return {
      restrict: 'E',
      transclude: true,
      replace: false,
      templateUrl: 'partials/media.html'
    }
  })

  .directive('post', function () {
    return {
      restrict: 'E',
      transclude: true,
      replace: false,
      templateUrl: 'partials/post.html'
    }
  })

  .directive('comment', function () {
    return {
      restrict: 'E',
      transclude: true,
      replace: false,
      templateUrl: 'partials/comment.html'
    }
  })

  .controller('PostDetailCtrl', function ($scope, $http, $sce, $route, $routeParams, $location, BACKEND_SERVER) {
    $scope.postId = $routeParams.postId;
    $http.get(BACKEND_SERVER + 'posts/' + $scope.postId + '\/')
      .then(function (res) {
        $scope.post = res.data;
        $scope.post.youtube = youtube_url_to_id($scope.post.url);
      });
    var success_callback = function (data, status, headers, config) {
    };
    var error_callback = function ($scope, data, status, headers, config) {
      console.log('error', data);
      $scope.status = status + ' ' + headers;
    };
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

      }).success(success_callback)
        .error(error_callback);
      $scope.formData = "";
      // TODO(pcsforeducation) remove when we get push comment add
      $route.reload();
    };
    $scope.trustSrc = function (src) {
      return $sce.trustAsResourceUrl(src);
    };
  })

  .controller('AuthCtrl', function ($scope, $rootScope, $location, httpInterceptor, authorization, api, AuthService, Auth, BACKEND_SERVER) {
    $scope.credentials = {
      username: '',
      password: ''
    };
    $scope.login = function (credentials) {
      Auth.setCredentials($rootScope, BACKEND_SERVER, credentials);
      $location.path('/posts').replace();
//      $scope.$apply();
      console.log('pathed');
//      $route.reload();
    };
    $scope.logout = function () {
      Auth.clearCredentials();
      $location.path('/login').replace();
//      $scope.$apply();
    };
    if (localStorage.getItem('token')) {
      $location.path('/posts').replace();
//      $scope.$apply();
    }
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
//      console.log('http intercepted');
      var success = function (response) {
        return response;
      };

      var error = function (response) {
        if (response.status === 401) {
          $location.path('/#/login');
//          $scope.$apply();
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

  .factory('Auth', ['Base64', '$http', '$rootScope', '$location', 'BACKEND_SERVER', function (Base64, $http, $rootScope, $location, BACKEND_SERVER) {
    // initialize to whatever is in the cookie, if anything
    $http.defaults.headers.common['Authorization'] = 'Token ' + localStorage.getItem('token');

    var success_function = function (data, status, headers, config) {
//      console.log('authdata', data);
      var token = data['token'];
      localStorage.setItem('token', token);
      localStorage.setItem('username', data['username']);
      $http.defaults.headers.common.Authorization = 'Token ' + token;
      $rootScope.loggedIn = true;
      $location.path('/posts');
//      $scope.$apply();
//      $rootScope.$apply();
    };

    var error_function = function (data, status, headers, config) {
      console.log('login error', status, headers);
    };

    return {
      setCredentials: function (scope, BACKEND_SERVER, credentials) {
        var encoded = Base64.encode(credentials['username'] + ':' + credentials['password']);
//        console.log('encoded', encoded, BACKEND_SERVER + 'token\/');
        $http({
          url: BACKEND_SERVER + 'token\/',
          method: "GET",
          headers: {
            'Authorization': 'Basic ' + encoded
          }
        }).success(success_function).error(error_function);
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
//        console.log('new post');
        $location.path('/#/posts').replace();
//        $scope.$apply();
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
    Chat.session.success(function (result) {
      $scope.session = result;
    });

    $scope.$watch(function () {
      var message_div = $('#chat_messages');
      message_div.scrollTop(message_div[0].scrollHeight);
    });

    // Handler to sending messages
    $scope.send_message = function () {
//      console.log($scope.text, $scope.session);
      $http({
        method: 'POST',
        url: BACKEND_SERVER + 'chat/messages\/',
        data: {'message': $scope.text}
      });
      $scope.text = "";
    };
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

  .directive('chat', function () {
    return {
      restrict: 'E',
      transclude: true,
      replace: false,
      templateUrl: 'partials/chat.html'
    }
  })

  .controller('PollListCtrl', function (BACKEND_SERVER) {
    $http.get(BACKEND_SERVER + 'polls\/')
      .then(function (res) {
        $scope.polls = res.data.results;
      });
  })

  .controller('PollDetailCtrl', function ($scope, $http, $routeParams, $location, User, BACKEND_SERVER) {
    $scope.pollStub = $routeParams.pollStub;
//    console.log('/#/polls/' + $scope.pollStub);
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
//        console.log('new post');
        $location.path('/#/polls/' + $scope.pollStub);
//        $scope.$apply();
      }).error(function ($scope, data, status, headers, config) {
        console.log('error', data);
        $scope.status = status + ' ' + headers;
      });
    };
    $scope.removeVote = function (id) {
      // Find the matching user vote
      var vote;
      $scope.user.user_votes.forEach(function(user_vote) {
        if (user_vote.submission == id) {
          vote = user_vote;
        }
      });
      if (vote == undefined) {
        console.log('Could not find matching vote for ', id);
        return
      }
      $http({
        url: BACKEND_SERVER + 'votes/' + vote.id + '\/',
        method: "DELETE",
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Authorization': 'Token ' + localStorage.getItem('token')
        }
      }).success(function (data, status, headers, config) {
        console.log('vote killed', data, vote);
        console.log('submissions', $scope.poll.poll_submissions)
        $scope.poll.poll_submissions.forEach(function(submission) {
          if (submission.id == vote.submission) {
            submission.voted = false;
          }
        });
      }).error(function ($scope, data, status, headers, config) {
        console.log('error', data);
      })
    };
    $scope.addVote = function (id) {
//      console.log('addVote');
      var data = {'submission': id, 'user': $scope.user.id};
//      console.log('submitting', data);
      $http({
        url: BACKEND_SERVER + 'votes\/',
        method: "POST",
        data: $.param(data),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Authorization': 'Token ' + localStorage.getItem('token')
        }
      }).success(function (data, status, headers, config) {
        console.log('new vote', data);
        $scope.user.user_votes.push(data);
        // Update the submission
        $scope.poll.poll_submissions.forEach(function(submission) {
          if (submission.id == data.submission) {
            submission.voted = true;
          }
        });
      }).error(function ($scope, data, status, headers, config) {
        console.log('error', data);
      })
    };

    $http.get(BACKEND_SERVER + 'polls/' + $scope.pollStub + '\/')
      .then(function (res) {
        $scope.poll = res.data;
        // find user
        var user;
        User.users.forEach(function(site_user) {
          if (localStorage.getItem('username') == site_user.username) {
            user = site_user;
          }
        });
        console.log('user is', user);

        $scope.poll.poll_submissions.forEach(function(submission) {
          console.log('sub votes', submission, user.user_votes);
          var voted = false;
          user.user_votes.forEach(function(vote) {
            if (vote.submission == submission.id) {
              voted = true;
            }
          });
          submission.voted = voted;
        })
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
        $location.path('/#/posts');
//        $scope.$apply();
      }).error(function ($scope, data, status, headers, config) {
        console.log('error', data);
        $scope.status = status + ' ' + headers;
      });
    }
  })

  .controller('NotificationCtrl', function ($scope, $http, Notification, BACKEND_SERVER) {
    $scope.notifications = [];
    $scope.notifications = Notification.notifications;
    $scope.remove_all = function () {
      Notification.remove_all();
      $scope.notifications = Notification.notifications;
    };
    $scope.remove_notification = function (item) {
      Notification.remove_notification(item);
    };
  })

  .controller('TabCtrl', function ($scope, $location, Channel) {
    $scope.tabs = [
      {'name': 'Posts', 'link': '/#/posts', 'alert': ''},
      {'name': 'Notifications', 'link': '/#/notifications', 'alert': ''},
      {'name': 'Chat', 'link': '/#/chat', 'alert': $scope.chat_count},
      {'name': 'BotD', 'link': '/#/polls/BotD', 'alert': ''},
      {'name': 'Profile', 'link': '/#/profile', 'alert': ''}
    ];

    // Highlight current tab
    var current_location = "/#" + $location.path();
    $scope.tabs.forEach(function (tab) {
      if (tab.link == current_location) {
        $scope.selected = tab;
      }
    });

    // Update highlighted tab when clicked
    $scope.select = function (item) {
      $scope.selected = item;
    };
    $scope.itemClass = function (item) {
      return item === $scope.selected ? 'active' : undefined;
    };

    // Update highlighted tab
    $scope.$on('$routeUpdate', function () {
//      console.log('route update')
    });

    // Bind chat alerts
    $scope.chat_count = Channel.stream.length;
  })
  .controller('OffCanvasDemoCtrl', function ($scope) {
  });

function removeChatIfAlreadyExists(chat, array) {
  var result = array.filter(function (potentialMatch) {
    return potentialMatch.id != chat.id;
  });

  return result;
}

function youtube_url_to_id(url) {
  if (!url) {
    return;
  }
  var vid = url.split('v=')[1];
  if (!vid) {
    return;
  }
  var ampersandPosition = vid.indexOf('&');
  if (ampersandPosition != -1) {
    vid = vid.substring(0, ampersandPosition);
  }
  return vid
}

