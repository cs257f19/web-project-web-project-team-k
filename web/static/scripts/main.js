// Disable empty form fields from GETting data
$('form').submit(function(e){
    var emptyinputs = $(this).find('input').filter(function(){
        return !$.trim(this.value).length;  // get all empty fields
    }).prop('disabled',true);
      var emptyselects = $(this).find('select').filter(function(){
          return !$.trim(this.value).length;  // get all empty fields
      }).prop('disabled',true);
});
