'use strict';

angular.module("ams", []).
  config(['$routeProvider', function($routeProvider){
    $routeProvider.when("/", {templateUrl:"static/partials/index.html", controller: IndexController}).
    when("/admin", {templateUrl:"static/partials/admin.html", controller: AdminController}).
    when("/songs/:songId", {templateUrl:"static/partials/view_song.html", controller: SongController}).
    when("/sign_up", {templateUrl:"static/partials/sign_up.html", controller: RegistrationController}).
    //$routeProvider.when("/signup", {templateUrl:"partials/signup.html", controller: SignupController}).
    otherwise({redirectTo:"/"});
}]);
