'use strict';

angular.module("ams", []).
  config(['$routeProvider', function($routeProvider){
    $routeProvider.when("/", {templateUrl:"static/partials/index.html", controller: IndexController}).
    when("/admin", {templateUrl:"static/partials/view_admin.html", controller: AdminController}).
    when("/songs/:songId", {templateUrl:"static/partials/view_song.html", controller: SongController}).
    when("/clerk", {templateUrl:"static/partials/view_clerk.html", controller: ClerkController}).
    when("/purchase", {templateUrl:"static/partials/view_purchase.html", controller: PurchaseController}).
    when("/checkout", {templateUrl:"static/partials/view_checkout.html", controller: CheckoutController}).
    //$routeProvider.when("/signup", {templateUrl:"partials/signup.html", controller: SignupController}).
    otherwise({redirectTo:"/"});
}]);
