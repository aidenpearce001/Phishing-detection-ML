(function($) {
  "use strict";
  
   $(document).ready(function() {
     
    $("#owl-demo").owlCarousel({
     
    navigation : false, // Show next and prev buttons
    slideSpeed : 3000,
	autoPlay: false,
    paginationSpeed : 400,
	transitionStyle:"fadeUp",
    singleItem:true
     
    // "singleItem:true" is a shortcut for:
    // items : 1,
    // itemsDesktop : false,
    // itemsDesktopSmall : false,
    // itemsTablet: false,
    // itemsMobile : false
     
    });
     
	 
	 $("#owl-demo2").owlCarousel({
     
    navigation : false, // Show next and prev buttons
    slideSpeed : 3000,
	autoPlay: false,
    paginationSpeed : 400,
    singleItem:true
     
    });
	
	$("#owl-demo3").owlCarousel({
     
    navigation : false, // Show next and prev buttons
    slideSpeed : 3000,
	autoPlay: false,
    paginationSpeed : 400,
    singleItem:true
     
    });
	
	$("#owl-demo4").owlCarousel({
     
    navigation : false, // Show next and prev buttons
    slideSpeed : 3000,
	autoPlay: false,
    paginationSpeed : 400,
    singleItem:true
     
    });
	
	

     
    $("#owl-demo5").owlCarousel({
     
    autoPlay: 3000, //Set AutoPlay to 3 seconds
     
    items : 4,
    itemsDesktop : [1199,3],
    itemsDesktopSmall : [979,3]
     
    });


$("#owl-demo6").owlCarousel({
    autoPlay : 3000,
    stopOnHover : true,
    navigation:true,
    paginationSpeed : 1000,
    goToFirstSpeed : 2000,
    singleItem : true,
    autoHeight : true,
    transitionStyle:"fadeUp"
  });
  
/*	  
	  

	 $("#owl-demo7").owlCarousel({
 
	navigation : true, // Show next and prev buttons
	slideSpeed : 1000,
	paginationSpeed : 400,
	singleItem:true,
	transitionStyle : "goDown"
 
});
*/

$("#owl-demo7").owlCarousel({

      navigation : true, // Show next and prev buttons
      slideSpeed : 1000,
      paginationSpeed : 400,
      singleItem:true,
	  transitionStyle : "goDown"

      // "singleItem:true" is a shortcut for:
      // items : 1, 
      // itemsDesktop : false,
      // itemsDesktopSmall : false,
      // itemsTablet: false,
      // itemsMobile : false

  });




//Sort random function
function random(owlSelector){
owlSelector.children().sort(function(){
return Math.round(Math.random()) - 0.5;
}).each(function(){
$(this).appendTo(owlSelector);
});
}
 
$("#owl-demo8").owlCarousel({
navigation: true,
slideSpeed : 700,
pagination:false,
navigationText: [
"prev",
"next"
],
beforeInit : function(elem){
//Parameter elem pointing to $("#owl-demo")
random(elem);
}
 
});

$("#owl-demo9").owlCarousel({

      navigation : true, // Show next and prev buttons
      slideSpeed : 1000,
      paginationSpeed : 400,
      singleItem:true,
	  pagination:false,
	  transitionStyle : "goDown"

      // "singleItem:true" is a shortcut for:
      // items : 1, 
      // itemsDesktop : false,
      // itemsDesktopSmall : false,
      // itemsTablet: false,
      // itemsMobile : false

  });

$("#owl-demo10").owlCarousel({

      navigation : true, // Show next and prev buttons
      slideSpeed : 1000,
      paginationSpeed : 400,
      singleItem:true,
	  pagination:true,
	  navigation : false,
	  transitionStyle : "fadeUp"

  });


	var sync1 = $("#sync1");
	var sync2 = $("#sync2");
	
	sync1.owlCarousel({
	singleItem : true,
	slideSpeed : 1000,
	pagination:false,
	afterAction : syncPosition,
	responsiveRefreshRate : 200,
	});
	
	sync2.owlCarousel({
	items : 5,
	itemsDesktop      : [1170,4],
	itemsDesktopSmall     : [979,4],
	itemsTablet       : [768,3],
	itemsMobile       : [479,2],
	pagination:false,
	responsiveRefreshRate : 100,
	afterInit : function(el){
	  el.find(".owl-item").eq(0).addClass("synced");
	}
	});
	
	function syncPosition(el){
	var current = this.currentItem;
	$("#sync2")
	  .find(".owl-item")
	  .removeClass("synced")
	  .eq(current)
	  .addClass("synced")
	if($("#sync2").data("owlCarousel") !== undefined){
	  center(current)
	}
	
	}
	
	$("#sync2").on("click", ".owl-item", function(e){
	e.preventDefault();
	var number = $(this).data("owlItem");
	sync1.trigger("owl.goTo",number);
	});
	
	function center(number){
	var sync2visible = sync2.data("owlCarousel").owl.visibleItems;
	
	var num = number;
	var found = false;
	for(var i in sync2visible){
	  if(num === sync2visible[i]){
		var found = true;
	  }
	}
	
	if(found===false){
	  if(num>sync2visible[sync2visible.length-1]){
		sync2.trigger("owl.goTo", num - sync2visible.length+2)
	  }else{
		if(num - 1 === -1){
		  num = 0;
		}
		sync2.trigger("owl.goTo", num);
	  }
	} else if(num === sync2visible[sync2visible.length-1]){
	  sync2.trigger("owl.goTo", sync2visible[1])
	} else if(num === sync2visible[0]){
	  sync2.trigger("owl.goTo", num-1)
	}
	}



	
    });
	
	})(jQuery);
