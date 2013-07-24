'use strict';

angular.module("ams", []).
  config(['$routeProvider', function($routeProvider){
    $routeProvider.when("/", {templateUrl:"static/partials/index.html", controller: IndexController}).
    when("/admin", {templateUrl:"static/partials/admin.html", controller: AdminController}).
    //$routeProvider.when("/signup", {templateUrl:"partials/signup.html", controller: SignupController}).
    otherwise({redirectTo:"/"});
}]);
