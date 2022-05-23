$(document).ready(function() {
    $( "#dialog-critical" ).dialog({
        autoOpen: false,
        modal: true,
        buttons: {
          Ok: function() {
            $( this ).dialog( "close" );
          }
        }
      });
      $( "#dialog-low" ).dialog({
        autoOpen: false,
        modal: true,
        buttons: {
          Ok: function() {
            $( this ).dialog( "close" );
          }
        }
      });
      $( "#dialog-high" ).dialog({
        autoOpen: false,
        modal: true,
        buttons: {
          Ok: function() {
            $( this ).dialog( "close" );
          }
        }
      });
      $( "#dialog-critical-temp" ).dialog({
        autoOpen: false,
        modal: true,
        buttons: {
          Ok: function() {
            $( this ).dialog( "close" );
          }
        }
      });
      $( "#dialog-low-temp" ).dialog({
        autoOpen: false,
        modal: true,
        buttons: {
          Ok: function() {
            $( this ).dialog( "close" );
          }
        }
      });
      $( "#dialog-high-temp" ).dialog({
        autoOpen: false,
        modal: true,
        buttons: {
          Ok: function() {
            $( this ).dialog( "close" );
          }
        }
      });
});