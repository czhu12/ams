'use strict';

function IndexController($scope, $http){
  $scope.hello = 'hello world';
  $http.get("api/songs").success(function(data){
    $scope.songs = data.songs;
  });
}

function RegistrationController($scope, $http){
}
function AdminController($scope, $http){
}
function ClerkController($scope, $http){

  $scope.credit=true;
  $scope.toggleCredit = function(){
    if(!$scope.credit){
      $scope.credit = true;
    }else{
      $scope.credit = false;
    }

  }
}

function SongController($scope, $routeParams){
  $scope.songId = $routeParams.songId;
  $scope.song = {
    upc:'1111111',
    title:'Starlight',
    type:'CD',
    artist:'Taylor Swift',
    category:'Classical',
    company:'company?',
    year:'2012',
    price:0.99,
    stock:100,
    thumbUrl:"http://wac.450f.edgecastcdn.net/80450F/popcrush.com/files/2012/10/RED-single.jpg"
  }
  $scope.purchase(){
    $http({
      method:"POST", 
      url:"/song/" + $scope.song.upc + "/purchase",
      data:""
    });
  }
  //$http.get("api/songs/" + $routeParams.songId).success(function(data){
  //  $scope.song = data.song;
  //});
}
