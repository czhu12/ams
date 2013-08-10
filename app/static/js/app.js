'use strict';

angular.module("ams", []).
  config(['$routeProvider', function($routeProvider){
    $routeProvider.when("/", {templateUrl:"static/partials/index.html", controller: IndexController}).
    when("/admin", {templateUrl:"static/partials/view_admin.html", controller: AdminController}).
    when("/songs/:songUpc", {templateUrl:"static/partials/view_song.html", controller: SongController}).
    when("/clerk", {templateUrl:"static/partials/view_clerk.html", controller: ClerkController}).
    when("/clerk/register", {templateUrl:"static/partials/view_clerk_register.html", controller: ClerkRegisterController}).
    when("/clerk/refund", {templateUrl:"static/partials/view_clerk_refund.html", controller: ClerkRefundController}).
    when("/checkout", {templateUrl:"static/partials/view_checkout.html", controller: CheckoutController}).
    when("/advanced", {templateUrl:"static/partials/view_advanced.html", controller: AdvancedController}).
    //$routeProvider.when("/signup", {templateUrl:"partials/signup.html", controller: SignupController}).
    otherwise({redirectTo:"/"});
}]);
