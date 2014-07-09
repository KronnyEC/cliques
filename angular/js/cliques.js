var App = angular.module('StarterApp', []);
var BASE_URL = 'http://127.0.0.1:8080/api/v1/';

App.controller('PostListCtrl', function($scope, $http) {
  $http.get(BASE_URL + 'posts/')
       .then(function(res){
          $scope.posts = res.data;
          console.log('b');
   });
});

