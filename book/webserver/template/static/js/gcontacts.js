var url = (window.location.protocol==="https):"?"wss://":"ws://") + window.location.host + '/ws/';
RPC = new WSRPC(url, 8080);
RPC.connect();

$(document).ready(function(){
    load_contacts_table();

    // filter for contacts table
    $("#contact-search-input").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#contacts-table tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

function load_contacts_table(){
    RPC.call('list_people').then(function (result) {
        data = JSON.parse(result)

        $('#contacts-table tbody').empty();

        for (i=0; i < data['len']; i++) {
            console.log(data['contacts'][i]);
            ref = data['contacts'][i]['resourceName']
            name = data['contacts'][i]['name']
            title = data['contacts'][i]['title']
            short_code = ''
            phone = ''
            extension = ''
            email = ''

            if ( data['contacts'][i]['contactNumbers']['len'] > 0 ) {
                for (pl=0; pl < data['contacts'][i]['contactNumbers']['len']; pl++) {
                    if ( data['contacts'][i]['contactNumbers']['phoneNumbers'][pl]['type'] === 'pager') {
                        short_code = data['contacts'][i]['contactNumbers']['phoneNumbers'][pl]['value']
                    } else if ( data['contacts'][i]['contactNumbers']['phoneNumbers'][pl]['type'] === 'mobile')  {
                        phone = data['contacts'][i]['contactNumbers']['phoneNumbers'][pl]['value']
                    } else if ( data['contacts'][i]['contactNumbers']['phoneNumbers'][pl]['type'] === 'Telephone Extension')  {
                        extension = data['contacts'][i]['contactNumbers']['phoneNumbers'][pl]['value']
                    }
                }
            }

            if (data['contacts'][i]['emailsAddresses']['len'] > 0){
                for (el=0; el < data['contacts'][i]['emailsAddresses']['len']; el++){
                    email = data['contacts'][i]['emailsAddresses']['emails'][el]['value']
                }
            }

            table_row = '<tr><th>' + (i + 1) + '</th><td><a data-toggle="modal" data-target="#ContactDetailedModal" data-contact-ref="' + ref + '" onclick="load_cMod_data(this);">'+ name +'</a></td><td>' + title + '</td><td>' + phone + '</td><td>' + short_code + '</td><td>' + extension + '</td><td>' + email + '</td></tr>'
            $('#contacts-table > tbody:last-child').append(table_row);
        }
    });
}

function load_cMod_data(identifier){
    resource_name = $(identifier).data('contact-ref');
     $('#contact-delete-button').data('resource-name', resource_name);

    RPC.call('get_people', {'resource_name' : resource_name}).then(function (result) {
        data = JSON.parse(result)
        console.log(data);
        $('#ContactDetailedModal').find('.modal-title').text(data['names'][0]['displayName']);
        $('#contacts-phone-card').empty();
        $('#contacts-email-card').empty();
        $('#contacts-organization-card').empty();

        if (data.hasOwnProperty('phoneNumbers')){
            for (i = 0; i < data['phoneNumbers'].length; ++i) {
                $("#contacts-phone-card").append('<label class="text-capitalize">' + data['phoneNumbers'][i]['type'] + '</lable><input type="text" class="form-control" value="' + data['phoneNumbers'][i]['value']  + '">');
            }
        }

        if (data.hasOwnProperty('emailAddresses')){
            for (i = 0; i < data['emailAddresses'].length; ++i) {
                $("#contacts-email-card").append('<label class="text-capitalize">' + data['emailAddresses'][i]['type'] + '</lable><input type="text" class="form-control" value="' + data['emailAddresses'][i]['value']  + '">');
            }
        }

        if (data.hasOwnProperty('organizations')){
            for (i = 0; i < data['organizations'].length; ++i) {
                $("#contacts-organization-card").append('<label class="text-capitalize">Name</lable><input type="text" class="form-control" value="' + data['organizations'][i]['name']  + '"><label class="text-capitalize">Title</lable><input type="text" class="form-control" value="' + data['organizations'][i]['title'] + '">');
            }
        }
    });
}

function delete_contact(identifier){
    resource_name = $(identifier).data('resource-name');

    $.confirm({
        title: 'Confirm Deleting Contact!',
        content: 'Confirm Deleting Contact',
        type: 'red',
        closeIcon: true,
        typeAnimated: true,
        draggable: true,
        buttons: {
            confirm: function () {
                RPC.call('delete_people', {'resource_name' : resource_name}).then(function (result) {
                    console.log(result);
                    load_contacts_table();
                });
                $.alert('The Contact has been Deleted!');
                $('#ContactDetailedModal').modal('hide');
            },
        }
    });
}

function new_contact(){
    $('#ContactNewModal').modal('hide');

    data_json = {
        'family_name': $('#newContactFirstName').val(),
        'given_name': $('#newContactLastName').val(),
        'mobile': $('#newContactMobile').val(),
        'pager': $('#newContactPager').val(),
        'extension': $('#newContactTExtension').val(),
        'work_email': $('#newContactWorkMail').val(),
        'personal_email': $('#newContactPersonalMail').val(),
        'work_name': $('#newContactWName').val(),
        'title': $('#newContactTitle').val()
    }

    RPC.call('create_people', {'data' : data_json}).then(function (result) {
        console.log(result);
        $.alert('Addition of the contact has been requested to server!');
    });

    load_contacts_table();
    $('#newContactFirstName').val('');
    $('#newContactLastName').val('');
    $('#newContactMobile').val('');
    $('#newContactPager').val('');
    $('#newContactTExtension').val('');
    $('#newContactWorkMail').val('');
    $('#newContactPersonalMail').val('');
    $('#newContactWName').val('');
    $('#newContactTitle').val('');
}

function export_contacts(){
    $("#contacts-table").csvExport({escapeContent:false});
}

// new contact form validations
function save_button_enable_check(){
    if ( ($('#newContactFirstName').val() === '') || ($('#newContactLastName').val() === '') ||  ($('#newContactMobile').val() === '') || ($('#newContactPager').val() === '') || ($('#newContactTitle').val() === '') ){
        $('#contact-new-button').prop('disabled', true);
    } else {
        $('#contact-new-button').prop('disabled', false);
    }
}

$("#newContactFirstName").on("change paste keyup", function() {
    save_button_enable_check();
});

$("#newContactLastName").on("change paste keyup", function() {
    save_button_enable_check();
});

$("#newContactMobile").on("change paste keyup", function() {
    save_button_enable_check();
});

$("#newContactPager").on("change paste keyup", function() {
    save_button_enable_check();
});

$("#newContactTitle").on("change paste keyup", function() {
    save_button_enable_check();
});