(function($) {
  "use strict";
  
  jQuery(document).ready(function($){

			$(".accordion_example1").smk_Accordion();

			$(".accordion_example2").smk_Accordion({
				closeAble: true, //boolean
			});

			$(".accordion_example3").smk_Accordion({
				showIcon: false, //boolean
			});

			$(".accordion_example4").smk_Accordion({
				closeAble: true, //boolean
				closeOther: false, //boolean
			});

			$(".accordion_example5").smk_Accordion({closeAble: true});

			$(".accordion_example6").smk_Accordion();
			
			$(".accordion_example7").smk_Accordion({
				activeIndex: 2 //second section open
			});
			$(".accordion_example8, .accordion_example9").smk_Accordion();

		});
		
		})(jQuery);