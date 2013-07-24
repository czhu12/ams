'use strict';

function IndexController($scope, $http){
  $scope.songs = [{
    name:"Fortune Teller",
    album:"Overexposed",
    artist:"Maroon 5"
  },
  {
    name:"Gold",
    album:"The Heist",
    artist:"Macklemore"
  }];
  //$http.get("ap1/books.json").success(function(data){
  //  $scope.books = data;
  //});
  //$http.get("ap1/scores.json").success(function(data){
  //  $scope.scores = data;
  //});
  //$http.get("ap1/cdordvd.json").success(function(data){
  //  $scope.cdordvd = data;
  //});
}

function AdminController($scope, $http){
}
