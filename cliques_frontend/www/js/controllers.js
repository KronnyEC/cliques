var BASE_URL = 'http://127.0.0.1:8080/api/v1/';

angular.module('starter.controllers', [])

.controller('AppCtrl', function($scope) {
})

.controller('PostListCtrl', function($scope, $http) {
  $http.get(BASE_URL + 'posts/')
       .then(function(res){
          $scope.posts = res.data;
          console.log('b');
  });
})

.controller('PostListCtrl', function($scope, $stateParams) {
})
