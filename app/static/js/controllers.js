'use strict';

function IndexController($scope, $http, $routeParams){
  $scope.query = $routeParams.query;
  $http.get("/api/items").success(function(data){
    $scope.songs = data.data;
  });
}

function CustomerController($scope){
}

function AdvancedController($scope){}
function ManagerAddItemsController($scope, $http){

  console.log('ellol');
  $scope.selectedFlag = true;
  $scope.selectedItem = {upc:"", title:"", price:'', stock:''};
  $scope.resp = "";
  refresh();
  function refresh() {
    $http.get("api/items").success(function(data){
      $scope.items = data.data;
    });
  } 
  
  $scope.update = function(){
  $.post('/api/items/add',
  { 
    upc:$scope.selectedItem.upc, 
    quantity:$scope.newStock,
    price:$scope.newPrice 
  },  function(resp){
    refresh();
    console.log(resp);
    $scope.resp = resp;
  }
  );
  return false;
  }

  $scope.selectItem = function(item){
    $scope.selectedItem = item;
    $scope.selectedFlag = false;
    $scope.newPrice = item.price;
    $scope.newStock = 0;
  }
  


}

function ManagerSalesReportController($scope, $http){
  $scope.message = '';
  $scope.data_cat = [];

  function refresh() {
    $http.get("api/items").success(function(data){
      $scope.items = data.data;
    });
  } 
    $scope.title = "hello world";
    $scope.friends = [{name:'John', age:25}, {name:'M', age:28}];
    $scope.friends.concat([{name:'Chris', age:20}]);
    
    console.log('Sales report controller ');

    $("#sales_report").click(function(){
        console.log( $("#date") );
        $.post(
                '/api/manager/sales_report',
                {date:$scope.date},
                function(resp){
					if ('success' in resp){
						$scope.message = ''
                    	addToScope(resp['success']);
					} else {
						$scope.message = resp['error'];
					}
                    console.log('changing scope...');
                    refresh();
                }
        );
    });

    function addToScope(resp){
        $scope.title="hi";
        $scope.data_str = JSON.stringify(resp);
        $scope.data = JSON.parse($scope.data_str);
        $scope.data_cat = {}
        for ( var key in $scope.data ) {
            console.log( key );
            for( var item in $scope.data[key] ) {
                console.log($scope.data[key][item].upc );
                if(key in $scope.data_cat) {
                    $scope.data_cat[key].item_list.push($scope.data[key][item]);
                }
                else {
                    $scope.data_cat[key] = {item_list:[], total_units:0, total_sales:0 };
                    $scope.data_cat[key].item_list.push($scope.data[key][item]);
                }
                $scope.data_cat[key].total_units += parseInt($scope.data[key][item].units);
                $scope.data_cat[key].total_sales += parseFloat($scope.data[key][item].total);
            }
            console.log($scope.data_cat[key].item_list);
        }
    }
}

function ManagerTopItemsController($scope, $http){
	$scope.message = '';
	$scope.data = [];
	function refresh(){
    	$http.get("api/items/1000").success(function(data){
    	});
	}

	$scope.getTopItems = function(){
		var n = $("input[name='n']").val();
		var date = $("input[name='date']").val();
		if(date=='')
			return;
		$.get(
			'api/manager/top_items',
			{date: date, n:n},
			function(data){
				if ('success' in data){
					$scope.message = 'Top ' + n + ' items on ' + date + ' are';
					$scope.data = data['success'];
				} else {
					$scope.data = [];
					$scope.message = data['error'];
				}
				refresh();
			}
		);
	}
}


function ManagerProcessDeliveryController($scope){}
/*
function ManagerTopItemsController($scope){
    console.log('TopItemsController');
    $scope.data = 'data';
    $("#top_selling").click(function(){
        console.log('top_selling clicked');
        $.get(
                '/api/manager/top_item',
                {date:'2013-08-05'},
                {n:5},
                function(resp){
                    $scope.data = resp;
                    addToScope(resp);
                }
        );
    });
}
*/

function ManagerProcessDeliveryController($scope, $http){
  $scope.rids = [];
  $scope.items = [];
  $scope.selectedItem = {};
  $http.get("/api/outstanding").success(function(data){
    console.log(data);
    $scope.rids = data.data;
  });
  
$scope.update = function(){ 
	$.post(
	"/api/deliver_update",
	{date:$("input[name=deliverydate]").val(), receiptid:$scope.selectedItem.receiptid},
	function(resp){
		console.log(resp);
	});
}
  $scope.addRid = function(rid){
    $http.get("/api/purchase/" + rid.receiptid).success(function(data){
      console.log(data.data);
      $scope.items = data.data;
      $scope.selectedItem = rid;
    });
  }
}

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
  $scope.rids = [];
  $scope.items = [];
  $scope.id = -1;
  $scope.message = ''
  $http.get("/api/purchases").success(function(data){
    console.log(data);
    $scope.rids = data.data;
  });
  
  function refresh(){
	$http.get('api/items/1000').success(function(data){});
  }

  $scope.addRid = function(rid){
    $http.get("/api/purchase/" + rid.receiptid).success(function(data){
      console.log(data.data);
      $scope.items = data.data;
      $scope.id = rid.receiptid;
    });
  }

  $scope.returnItem = function(){
    if($scope.id==-1)
      return;
	var arr = ItemsArr();
	var trivial = true;
    $.each(arr, function(index){
		if(arr[index].quantity > 0)
			trivial = false;
	});
	if(trivial){
		$scope.message = "No items returned"
		return;
	}
    console.log({arr:JSON.stringify(ItemsArr()), receiptid:$scope.id});
	$.post(
	  'api/return',
      {arr:JSON.stringify(ItemsArr()), receiptid:$scope.id},
      function(resp){
		$scope.message = resp;
		$scope.addRid({receiptid: $scope.id});
      }
    );
  }

  function ItemsArr(){
	var arr = [];
    $.each($scope.items, function(index){
        var upc = $scope.items[index].upc;
		arr.push({upc:upc, quantity:$("input[name="+ upc +"]").val()});
	});
	return arr;
  }
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
  $scope.price = 0;
  $scope.selectedSongs = {};
  $scope.quantityChange = function(upc){
    console.log('hello' + upc);
  };

  var totalPrice = 0;

  function refresh(){
	$http.get('api/items/1000');
  }

  function computeTotalPrice(){
    totalPrice = 0;
    $.each($scope.selectedSongs, function(index, song){
      var quantity = parseFloat($("input[name=" + song.upc + "]").val());
      var price = parseFloat(song.price);
      totalPrice += quantity*price;
    });
  };

  $scope.purchase = function(){
	var arr = selectedSongsArr();
	if (arr.length == 0){
		return;
	}
	var arg = {'arr':JSON.stringify(selectedSongsArr())};

	if($("input[name='ccb']").is(':checked')){
		arg['credit'] = JSON.stringify({'cardnum':$("input[name='ccn']").val(), 'expirydate':$("input[name='cce']").val()});
		$.post('/api/store_purchase/credit', arg, function(resp){console.log(resp);} );
	} else {
		$.post('/api/store_purchase/cash', arg, function(resp){console.log(resp);} );
	}
    return false;
  }

  $("#clerk-selected-list").on('input', function(){
      computeTotalPrice();
      $("#totalprice").text(Math.round(totalPrice*100)/100);
  });

  $("button[name='get_price']").click(function(){
    $.get("/api/price",
		{arr:JSON.stringify(selectedSongsArr())},
		function(resp){
			$scope.price = resp;
			refresh();
			console.log(resp);
		}
	);
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

  function selectedSongsArr(){
	var arr = [];
    $.each($scope.selectedSongs, function(index, song){
		arr.push({upc:index, quantity:$("input[name="+ index +"]").val()});
	});
	return arr;
  }

}

function SongController($scope, $routeParams, $http){
  $scope.imgUrl = img_url[$routeParams.songUpc];
  console.log($scope.imgUrl);
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
