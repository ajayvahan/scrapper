$(document).ready(function(){
	$("#dashboard_form").submit(function(){
		$.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function(json_data) { // on success..
             $("#dashboard_result").html(json_data.result)
             console.log(json_data.result)
             console.log('success')
            },
            error: function(json_data) { // on error..
                 alert(Error)
                 console.log(json_data)
                 console.log('error')

            }
        });
        return false;
	});

    $("#scrap_form").submit(function(){
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function(json_data) { // on success..
             $("#scrap_result").html(json_data.result)
             console.log(json_data.result)
             console.log('success')
            },
            error: function(json_data) { // on error..
                 alert(Error)
                 console.log(json_data)
                 console.log('error')

            }
        });
        return false;
    });
})