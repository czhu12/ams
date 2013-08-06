'use strict';

function IndexController($scope, $http, $routeParams){
  $scope.query = $routeParams.query;
  $http.get("api/songs").success(function(data){
    $scope.songs = data.songs;
  });
}

function RegistrationController($scope, $http){
}
function PurchaseController($scope, $http, $routeParams){
  $scope.upc = $routeParams.upc;
  $http.get("api/songs/" + $scope.upc).success(function(data){
    $scope.song = data.song;
  });
}
function AdminController($scope, $http){
  $("#col2-admin").load("/static/partials/admin_partials/page1.html");
  $scope.page1 = function(){
    $("#col2-admin").load("/static/partials/admin_partials/page1.html");
  };
  $scope.page2 = function(){
    $("#col2-admin").load("/static/partials/admin_partials/page2.html");
  };
  $scope.page3 = function(){
    $("#col2-admin").load("/static/partials/admin_partials/page3.html");
  };
  $scope.page4 = function(){
    $("#col2-admin").load("/static/partials/admin_partials/page4.html");
  };
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

function SongController($scope, $routeParams, $http, $location){
  $scope.songId = $routeParams.songId;
  $scope.song = {
    upc:'1111111',
    title:'Starlight',
    type:'CD',
    artist:'Taylor Swift',
    album:"Red",
    category:'Classical',
    company:'company?',
    year:'2012',
    price:0.99,
    stock:100,
    thumbUrl:"http://wac.450f.edgecastcdn.net/80450F/popcrush.com/files/2012/10/RED-single.jpg"
  }
  $scope.purchase = function(){
    $http.post("/api/songs/" + $scope.song.upc + "/purchase", "").success(function(data, status, headers, config){
      window.location="#/purchase?upc=" + $scope.song.upc;
    });
  }
  $scope.search = function(query){
    window.location="#/?query=" + query;
  };
}
