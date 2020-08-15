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

            table_row = '<tr><th>' + (i + 1) + '</th><td>'+ name +'</td><td>' + title + '</td><td>' + phone + '</td><td>' + short_code + '</td><td>' + extension + '</td><td>' + email + '</td></tr>'
            $('#contacts-table > tbody:last-child').append(table_row);
        }
    });
}