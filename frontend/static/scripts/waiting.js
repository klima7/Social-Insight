function check() {
    $.ajax({
        dataType: "json",
        url: "/api/packs/last/status",
        cache: false,
        success: function(data) {
            console.log(data.status);
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
	setTimeout(() => {
		window.location.href = '/packs/last';
	}, 3000)
}

check();
