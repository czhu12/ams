'use strict';

function IndexController($scope, $http, $routeParams){
  $scope.query = $routeParams.query;
  $http.get("/api/items").success(function(data){
    $scope.songs = data.data;
  });
}

function AdvancedController($scope){}
function ManagerAddItemsController($scope){}

function ManagerSalesReportController($scope){
    $scope.title = "hello world";
    console.log('Sales report controller ');
    $("#sales_report").click(function(){
        console.log(' clicked');
        $.get(
                '/api/manager/sales_report',
                {date:'2013-08-10'},
                function(resp){
                    console.log(resp);
                    console.log($scope.title);
                    $scope.title = 'blah';
                    $scope.data = JSON.stringify(resp);
                }
        );
    });
}

function ManagerTopItemsController($scope){}
function ManagerProcessDeliveryController($scope){}

function ClerkController($scope, $location){
  $scope.purchase = function(){
    $location.path("/clerk/register");
  }
  
  $scope.refund = function(){
    $location.path("/clerk/refund");
  }
}

function CheckoutController($scope, $http){
  $http.get('api/checkout/expected').success(function(data){
    $scope.expected_date = data;
  });
  var cart = $.parseJSON($.cookie("cart"));
	$scope.upcs = {};
	var allItems;
	$http.get('api/items').success(function(data){
		allItems = data.data;
		$scope.selectedItems = {};
		for(var i = 0; i < allItems.length; i++){
		if (allItems[i].upc in cart) {
			$scope.selectedItems[allItems[i].upc] = {};
			$scope.selectedItems[allItems[i].upc].item = allItems[i];
			$scope.selectedItems[allItems[i].upc].quantity = cart[allItems[i].upc];
		}
	}
	console.log($scope.selectedItems);
	});
	
}

function ClerkRefundController($scope, $http){
  $http.get("api/songs/" + $scope.upc).success(function(data){
    $scope.song = data.song;
  });
}

function ManagerController($scope, $http, $location){
  $scope.addItem = function(){
    $location.path("/manager/add_items")
  }
  $scope.processDelivery = function(){
    $location.path("/manager/process_delivery")
  }
  $scope.salesReport = function(){
    $location.path("/manager/sales_report")
  }
  $scope.topItems = function(){
    $location.path("/manager/top_items")
  }
}
function ClerkRegisterController($scope, $http){
  $scope.selectedSongs = {};
  $scope.quantityChange = function(upc){
    console.log('hello' + upc);
  };

  var totalPrice = 0;

  function computeTotalPrice(){
    totalPrice = 0;
    $.each($scope.selectedSongs, function(index, song){
      var quantity = parseFloat($("input[name=" + song.upc + "]").val());
      var price = parseFloat(song.price);
      totalPrice += quantity*price;
    });
  };

  $scope.purchase = function(){
    var orders = [];
    $.each($(".selected-songs"), function(index, Element){
      var input = $(Element).find("input");
      var order = {
        upc: input.attr('name'),
        quantity: input.val()
      }; 
      orders.push(order);
    });
    console.log(JSON.stringify({'arr':orders}));
		$.post('/api/store_purchase', {'arr':JSON.stringify(orders)} );
    return false;
  }

  $("#clerk-main-list").on('input', function(){
      computeTotalPrice();
      $("#totalprice").text(Math.round(totalPrice*100)/100);
  });

  $http.get("/api/items").success(function(data){
    $scope.songs = data.data;
  });

  $scope.credit=true;
  $scope.toggleCredit = function(){
    if(!$scope.credit){
      $scope.credit = true;
    }else{
      $scope.credit = false;
    }
  };

  $scope.addUpc = function(upc){
		if(upc in $scope.selectedSongs){
			return;
		}

    for(var i = 0; i < $scope.songs.length; i++){
      if ($scope.songs[i].upc == upc){
        //$scope.selectedSongs.push($scope.songs[i]);
        $scope.selectedSongs[upc] = $scope.songs[i];
        totalPrice += parseFloat($scope.songs[i].price);
        break;
      }
    }
	
    $("#totalprice").text(Math.round(totalPrice*100)/100);
  }
  
  $scope.dropItem = function(upc){
    delete $scope.selectedSongs[upc];
  }

}

function SongController($scope, $routeParams, $http){
  $scope.validate = function(){
    console.log('validating...');
    if(isNaN(parseInt($scope.quantity))){
      $("input[name=quantity]").attr("class", "error-input");
      return;
    }

    $("input[name=quantity]").attr("class", "success-input");
  }

  $scope.calcPrice = function(quantity, price){
    if(isNaN(parseInt(quantity)))
      return 0;
    return Math.round(quantity * price * 100)/100;
  }

	$http.get("/api/items/" + $routeParams.songUpc).success(function(data){
		$scope.song = data.data[0];
  	if ($scope.song.stock === "0") {
    	$("#song-stock").css("color", "red");
  	}
	});
  
  $scope.addSongToCart = function(){
		if (($scope.quantity == "") || (isNaN(parseInt($scope.quantity)))){
			alert("Must specify a valid Quantity");
			return false;
		}
    
    var currentCart = $.parseJSON($.cookie("cart"));
		var writeQuan = parseInt($scope.quantity);
		if ($scope.song.upc in currentCart){
			var currentQuan = parseInt(currentCart[$scope.song.upc]);
			writeQuan = writeQuan + currentQuan;
		}
		currentCart[$scope.song.upc] = writeQuan;
		$.cookie("cart", JSON.stringify(currentCart), {expires:3, path:'/'});
    console.log($.cookie('cart'));
    window.location = "#/";
  };

  
  $scope.search = function(query){
    window.location="#/?query=" + query;
  };
}
