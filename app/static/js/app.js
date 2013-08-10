'use strict';

angular.module("ams", []).
  config(['$routeProvider', function($routeProvider){
    $routeProvider.when("/", {templateUrl:"static/partials/index.html", controller: IndexController}).
    when("/manager", {templateUrl:"static/partials/manager_partials/view_manager.html", controller: ManagerController}).
    when("/manager/add_items", {templateUrl:"static/partials/manager_partials/view_manager_add_items.html", controller: ManagerAddItemsController}).
    when("/manager/sales_report", {templateUrl:"static/partials/manager_partials/view_manager_sales_report.html", controller: ManagerSalesReportController}).
    when("/manager/top_items", {templateUrl:"static/partials/manager_partials/view_manager_top_items.html", controller: ManagerTopItemsController}).
    when("/manager/process_delivery", {templateUrl:"static/partials/manager_partials/view_manager_process_delivery.html", controller: ManagerProcessDeliveryController}).
    when("/songs/:songUpc", {templateUrl:"static/partials/view_song.html", controller: SongController}).
    when("/clerk", {templateUrl:"static/partials/view_clerk.html", controller: ClerkController}).
    when("/clerk/register", {templateUrl:"static/partials/view_clerk_register.html", controller: ClerkRegisterController}).
    when("/clerk/refund", {templateUrl:"static/partials/view_clerk_refund.html", controller: ClerkRefundController}).
    when("/checkout", {templateUrl:"static/partials/view_checkout.html", controller: CheckoutController}).
    when("/advanced", {templateUrl:"static/partials/view_advanced.html", controller: AdvancedController}).
    //$routeProvider.when("/signup", {templateUrl:"partials/signup.html", controller: SignupController}).
    otherwise({redirectTo:"/"});
}]);
