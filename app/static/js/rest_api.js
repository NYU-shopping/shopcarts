$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#item_id").val(res.id);
        $("#item_name").val(res.name);
        $("#item_sku").val(res.sku);
        if (res.available == true) {
            $("#item_available").val("true");
        } else {
            $("#item_available").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#item_name").val("");
        $("#item_sku").val("");
        $("#item_available").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create an Item
    // ****************************************

    $("#create-btn").click(function () {

        console.log("Creating an Item");

        var name = $("#item_name").val();
        var sku = $("#item_sku").val();
        var available = $("#item_available").val() == "true";

        var data = {
            "name": name,
            "sku": sku,
            "is_available": available
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/shopcarts/items",
            contentType:"application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update an Item
    // ****************************************

    $("#update-btn").click(function () {

        console.log("Updating an Item");

        var item_id = $("#item_id").val();
        var name = $("#item_name").val();
        var sku = $("#item_sku").val();
        var available = $("#item_available").val() == "true";

        var data = {
            "name": name,
            "sku": sku,
            "is_available": available
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/shopcarts/items/" + item_id,
                contentType:"application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve an Item
    // ****************************************

    $("#retrieve-btn").click(function () {

        console.log("Retrieving an Item");

        var item_id = $("#item_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts/items/" + item_id,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete an Item
    // ****************************************

    $("#delete-btn").click(function () {

        console.log("Deleting an Item");

        var item_id = $("#item_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/shopcarts/items/" + item_id,
            contentType:"application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Item with ID [" + res.id + "] has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {

        console.log("clearing the form");

        $("#item_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for an Item
    // ****************************************

    $("#search-btn").click(function () {

        console.log("searching for an item");

        var name = $("#item_name").val();
        var sku = $("#item_sku").val();
        var available = $("#item_available").val() == "true";

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (sku) {
            if (queryString.length > 0) {
                queryString += '&sku=' + sku
            } else {
                queryString += 'sku=' + sku
            }
        }
        
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }


        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts/items?" + queryString,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Sku</th>'
            header += '<th style="width:10%">Available</th></tr>'
            $("#search_results").append(header);
            for(var i = 0; i < res.length; i++) {
                item = res[i];
                var row = "<tr><td>"+item.id+"</td><td>"+item.name+"</td><td>"+item.sku+"</td><td>"+item.is_available+"</td></tr>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
