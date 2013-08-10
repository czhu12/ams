'use strict';

function IndexController($scope, $http, $routeParams){
  $scope.query = $routeParams.query;
  $http.get("/api/items").success(function(data){
    $scope.songs = data.data;
  });
}

function CheckoutController($scope, $http){
  var cart = $.parseJSON($.cookie("cart"));
  console.log(cart);
  //var songs = [];
  //for(var i = 0; i < cart.length; i++){
  //  var item = cart[i];
  //  $http.get("api/songs/" + item.upc).success(function(data){
  //    var song = data.song;
  //    song.quantity = item.quantity;
  //    songs.push(song);
  //  });
  //}

  //var totalPrice = 0;
  //for(var i = 0; i < songs.length; i++){
  //  totalPrice = totalPrice + (songs[i].quantity * songs[i].price);
  //}
  //$scope.totalPrice = totalPrice;
}
function PurchaseController($scope, $http, $routeParams){
  $scope.upc = $routeParams.upc;
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
function ClerkController($scope, $http){
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
    //console.log(orders);
    console.log(JSON.stringify({'arr':orders}));
    //$http.post('/api/store_purchase', {arr:JSON.stringify(orders)} );
		$.post('/api/store_purchase', {'arr':JSON.stringify(orders)} );
    return false;
  }

  $("#clerk-main-list").on('input', function(){
      computeTotalPrice();
      $("#totalprice").text("$" + totalPrice);
  });

  $http.get("/api/items").success(function(data){
    console.log(data.data);
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
    for(var i = 0; i < $scope.songs.length; i++){
      if ($scope.songs[i].upc == upc){
        //$scope.selectedSongs.push($scope.songs[i]);
        $scope.selectedSongs[upc] = $scope.songs[i];
        totalPrice += parseFloat($scope.songs[i].price);
        break;
      }
    }
    $("#totalprice").text("$" + totalPrice);
  }
  
  $scope.dropItem = function(upc){
    console.log('lick');
    delete $scope.selectedSongs[upc];
  }

}

function SongController($scope, $routeParams, $http, $location){
	console.log($routeParams.songUpc);
  $scope.calcPrice = function(quantity, price){
    if(isNaN(parseInt(quantity)))
      return 0;
    return Math.round(quantity * price * 100)/100;
  }
	$http.get("/api/items").success(function(){
	
	});
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
    stock:10,
    thumbUrl:"http://wac.450f.edgecastcdn.net/80450F/popcrush.com/files/2012/10/RED-single.jpg"
  };

  if ($scope.song.stock == 0) {
    $("#song-stock").css("color", "red");
  }
  
  $scope.addSongToCart = function(){
    var currentList = $.parseJSON($.cookie("cart"));
    currentList.push({
      upc: $scope.song.upc,
      quantity: $scope.quantity });
    $.cookie("cart", JSON.stringify(currentList), {expires:3, path:'/'});
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
