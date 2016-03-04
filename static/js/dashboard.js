$(document).ready(function(){
    // Make an ajax call when dashboard form is submitted
	$("#dashboard_form").submit(function(){
		$.ajax({ // Create an AJAX call...
            data: $(this).serialize(), // Get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            beforeSend: function(){
                    $('#dashboard-result').html(''); // Clear dashboard result div
                    $("#dashboard-loading").show(); // Show loading gif
            },
                complete: function(){
                    $("#dashboard-loading").hide(); // Hide loading gif
            },
            success: function(json_data) { // On success..
             $("#dashboard-result").html(json_data.result)
             console.log(json_data.result)
             console.log('success')
            },
            error: function(json_data) { // On error..
                 alert(Error)
                 console.log(json_data)
                 console.log('error')

            }
        });
        return false;
	});

    $("#scrap_form").submit(function(){
        $.ajax({ // Create an AJAX call...
            data: $(this).serialize(), // Get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // The file to call
            beforeSend: function(){
                    $('#scrap-result').html(''); // Clear dashboard result div
                    $("#scrap-loading").show(); // Show loading gif
            },
                complete: function(){
                    $("#scrap-loading").hide(); // Hide loading gif
            },
            success: function(json_data) { // On success..
             $("#scrap-result").html(json_data.result)
             console.log(json_data.result)
             console.log('success')
            },
            error: function(json_data) { // On error..
                 alert(Error)
                 console.log(json_data)
                 console.log('error')

            }
        });
        return false;
    });
})