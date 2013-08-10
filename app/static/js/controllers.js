'use strict';

function IndexController($scope, $http, $routeParams){
  $scope.query = $routeParams.query;
  $http.get("/api/items").success(function(data){
    $scope.songs = data.data;
  });
}

function AdvancedController($scope){}

function ClerkController($scope){
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

function AdminController($scope, $http){
  $scope.test = "hello";

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
    //$http.post('/api/store_purchase', {arr:JSON.stringify(orders)} );
		$.post('/api/store_purchase', {'arr':JSON.stringify(orders)} );
    return false;
  }

  $("#clerk-main-list").on('input', function(){
      computeTotalPrice();
      $("#totalprice").text(totalPrice);
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
	
    $("#totalprice").text(totalPrice);
  }
  
  $scope.dropItem = function(upc){
    delete $scope.selectedSongs[upc];
  }

}

function SongController($scope, $routeParams, $http){
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
		if (($scope.quantity == "") || (typeof $scope.quantity != "string")){
			alert("Must specify a Quantity");
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

  //$scope.purchase = function(){
  //  $http.post("/api/songs/" + $scope.song.upc + "/purchase", "").success(function(data, status, headers, config){
  //    window.location="#/purchase?upc=" + $scope.song.upc;
  //  });
  //};
  $scope.search = function(query){
    window.location="#/?query=" + query;
  };
}
