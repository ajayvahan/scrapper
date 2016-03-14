$(document).ready(function(){
    // Make an ajax call when dashboard form is submitted
	$("#dashboard_form").submit(function(){
		$.ajax({ // Create an AJAX call...
            data: $(this).serialize(), // Get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            beforeSend: function(){
                $('#dashboard-result').html(''); // Clear dashboard result div
                $('input[type=radio]').prop('checked', false);
                $('#id_amazon').prop('checked', false);
                $('#id_flipkart').prop('checked', false); // Unchecks it
                $("#dashboard-loading").show(); // Show loading gif
            },
            complete: function(){
                $("#dashboard-loading").hide(); // Hide loading gif
                $("#filter-section").show();
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
                $('#scrap-result').html(''); // Clear dashboard result d
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

    $(".filter-click").click(function(){
        $.ajax({ // create an AJAX call...
            data: $("#filter_form").serialize(), // get the form data
            type: $("#filter_form").attr('method'), // GET or POST
            url: $("#filter_form").attr('action'), // the file to call
            beforeSend: function(){
                    $('#dashboard-result').html('');
                    $("#dashboard-loading").show();
            },
            complete: function(){
                    $("#dashboard-loading").hide();
            },
            success: function(json_data) { // on success..
             $("#dashboard-result").html(json_data.result)
             console.log(json_data.result)
             console.log('success')
            },
            error: function(json_data) { // on error..
                 alert(Error)
                 console.log(json_data)
                 console.log('error')
            }
        });
        return true;
    });

     // ajax for changing the total on changing the quantity
    $("#id_quantity").change(function(){
        $.ajax({ // create an AJAX call...
            data: $("#summary_form").serialize(), // get the form data
            type: $("#summary_form").attr('method'), // GET or POST
            url: $("#summary_form").attr('action'), // the file to call
            success: function(response) { // on success..
                if (response.success){
                   console.log(response.message);
                    $('#total_price').html(response.total_price);
                    $('#summary_continue_button').removeClass('disabled')

                }
                else{
                    alert(response.message);
                    $('#summary_continue_button').addClass('disabled')
                }
                
            },
            error: function(response) { // on error..
                alert(response.message)
            }
        });
        return false;
    });
})