jQuery(document).ready(function(){
    
    jQuery('#sparkline').sparkline([4,3,3,1,4,3,2,2,3,10,9,6], {
		  type: 'bar', 
		  height:'30px',
        barColor: '#428BCA'
    });
	
    
    jQuery('#sparkline2').sparkline([9,8,8,6,9,10,6,5,6,3,4,2], {
		  type: 'bar', 
		  height:'30px',
        barColor: '#999'
    });
    
    
    jQuery('#table1').dataTable({
      "iDisplayLength": 5,
      "bLengthChange": false
    });
    
    // Chosen Select
    jQuery("select").chosen({
      'min-width': '100px',
      'white-space': 'nowrap',
      disable_search_threshold: 10
    });
    
});