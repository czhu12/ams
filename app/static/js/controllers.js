'use strict';

function IndexController($scope, $http){
  $http.get("api/songs").success(function(data){
    $scope.songs = data.songs;
  });
}

function RegistrationController($scope, $http){
}
function AdminController($scope, $http){
}

function SongController($scope, $routeParams){
  $scope.songId = $routeParams.songId;
  $scope.song = {
    upc:'1111111',
    title:'Starlight',
    type:'CD',
    category:'classical',
    company:'company?',
    year:'2012',
    price:0.99,
    stock:100,
    thumbUrl:"http://wac.450f.edgecastcdn.net/80450F/popcrush.com/files/2012/10/RED-single.jpg"
  }
  //$http.get("api/songs/" + $routeParams.songId).success(function(data){
  //  $scope.song = data.song;
  //});
}
