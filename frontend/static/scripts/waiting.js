let packid = $('#packid').text()

function check() {
    $.ajax({
        dataType: "json",
        url: `/api/packs/${packid}/status`,
        cache: false,
        success: function(data) {
            if(data.status == 'success') {
                redirect();
            }
            else if(data.status == 'pending' || data.status == 'processing') {
                setTimeout(check, 1000);
            }
            else {
            	alert(`Error: pack status is ${data.status}`)
            }
        },
        error: function() {
            alert("Error occured on ready check");
        }
    });
}

function redirect() {
	window.location.href = `/packs/${packid}`;
}

setTimeout(check, 2000);
