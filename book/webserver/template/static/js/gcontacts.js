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
    RPC.call('get_people', {'resource_name' : resource_name}).then(function (result) {
        data = JSON.parse(result)
        console.log(data);
        $('#ContactDetailedModal').find('.modal-title').text(data['names'][0]['displayName']);
        $('#contacts-phone-card').empty();
        $('#contacts-email-card').empty();
        $('#contacts-organization-card').empty();

        if (data.hasOwnProperty('phoneNumbers')){
            for (i = 0; i < data['phoneNumbers'].length; ++i) {
                $("#contacts-phone-card").append('<h6 class="card-subtitle mb-2 text-muted text-capitalize">' + data['phoneNumbers'][i]['type'] + '</h6><p class="card-text">' + data['phoneNumbers'][i]['value']  + '</p>');
            }
        }

        if (data.hasOwnProperty('emailAddresses')){
            for (i = 0; i < data['emailAddresses'].length; ++i) {
                $("#contacts-email-card").append('<h6 class="card-subtitle mb-2 text-muted text-capitalize">' + data['emailAddresses'][i]['type'] + '</h6><p class="card-text">' + data['emailAddresses'][i]['value']  + '</p>');
            }
        }

        if (data.hasOwnProperty('organizations')){
            for (i = 0; i < data['organizations'].length; ++i) {
                $("#contacts-organization-card").append('<h6 class="card-subtitle mb-2 text-muted text-capitalize">Name</h6><p class="card-text">' + data['organizations'][i]['name']  + '</p><h6 class="card-subtitle mb-2 text-muted text-capitalize">Title</h6><p class="card-text">' + data['organizations'][i]['title'] + '</p>');
            }
        }
    });
}