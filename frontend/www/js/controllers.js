var BASE_URL = 'http://127.0.0.1:8080/api/v1/';

angular.module('post_controllers', [])

.controller('PostListCtrl', function($scope, $http, $location) {
    // Get data on startup
    $http.get(BASE_URL + 'posts/')
        .then(function(res){
            $scope.posts = res.data.results;
            console.log($scope.posts);
    });
})

.controller('AuthCtrl', function ($scope, $rootScope, $location, $cookieStore, httpInterceptor, authorization, api, AuthService, Auth) {
    $scope.credentials = {
        username: '',
        password: ''
    };
    $scope.login = function (credentials) {
        Auth.setCredentials(credentials);
        $location.path('/#/posts');
    };
})
.filter('DTSince', function() {
    return function(dt) {
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
.factory('httpInterceptor', function httpInterceptor ($q, $window, $location) {
  return function (promise) {
      console.log('http intercepted');
      var success = function (response) {
          return response;
      };

      var error = function (response) {
          if (response.status === 401) {
              $location.url('/login');
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
.factory('Auth', ['Base64', '$cookieStore', '$http', function (Base64, $cookieStore, $http) {
    // initialize to whatever is in the cookie, if anything
    $http.defaults.headers.common['Authorization'] = 'Basic ' + $cookieStore.get('authdata');

    return {
        setCredentials: function (credentials) {
            var encoded = Base64.encode(credentials['username'] + ':' + credentials['password']);
            $http.defaults.headers.common.Authorization = 'Basic ' + encoded;
            $cookieStore.put('authdata', encoded);
        },
        clearCredentials: function () {
            document.execCommand("ClearAuthenticationCache");
            $cookieStore.remove('authdata');
            $http.defaults.headers.common.Authorization = 'Basic ';
        }
    };
}])
.factory('Base64', function() {
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
.controller('PostDetailCtrl', function() {

})
.controller('NewPostCtrl', function($scope, $http, $location) {
    $scope.formData = {};
    $scope.new_post_submit = function() {
        console.log("submit");
        $http({
            url: BASE_URL + 'posts\/',
            method: "POST",
            data:  $.param($scope.formData),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
        }).success(function (data, status, headers, config) {
            $location('/#/posts')
        }).error(function (data, status, headers, config) {
            $scope.status = status + ' ' + headers;
        });
    }
});

