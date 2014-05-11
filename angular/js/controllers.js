var App = angular.module('CliquesApp', []);

App.controller('PostListController', function($scope, $http) {
  $http.get('todos.json')
       .then(function(res){
          $scope.todos = res.data;
        });
});