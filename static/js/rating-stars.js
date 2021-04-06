$('.stars .fa-star').click(function() {
    let id = $(this).attr('id');
    let url = $(this).parent().find('.url-to-rate').text();
    let token = $('input[name=csrfmiddlewaretoken]').val();
    let book_id = id.split("_")[1];
    let rating = id.split("_")[2];

    $.ajax(url, {
        type: "POST",
        data: {rating:rating,csrfmiddlewaretoken:token},
        statusCode: {
            200: function (response) {
                let js  = JSON.parse(response);

                let my_rating = parseFloat(js['my'])

                // update rating
                $('#avg_' + book_id).text(js['avg']);


                // recheck stars
                $('.star-' + book_id).removeClass('checked')

                if(my_rating > 0.5)
                {
                    $('#stars_' + book_id + '_1').addClass('checked')
                }
                if(my_rating > 1.5)
                {
                    $('#stars_' + book_id + '_2').addClass('checked')
                }
                if(my_rating > 2.5)
                {
                    $('#stars_' + book_id + '_3').addClass('checked')
                }
                if(my_rating > 3.5)
                {
                    $('#stars_' + book_id + '_4').addClass('checked')
                }
                if(my_rating > 4.5)
                {
                    $('#stars_' + book_id + '_5').addClass('checked')
                }


            },
            405: function (response) {
                alert(response);
            },
            400: function (response) {
                alert(response);
            },
            404: function (response) {
                alert(response);
            },
        }, success: function () {
            // alert('1');
        },


    });

});