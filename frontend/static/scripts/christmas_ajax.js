function toggleChristmasEvent(graphid, collationid) {
	let active = isChristmasButtonActive();
	setChristmas(!active);
}

function setChristmas(status) {
    $.ajax({
    	method: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        url: '/api/christmas',
        cache: false,
        data: JSON.stringify({'status': status}),
        success: function(data) {
			setChristmasButtonActive(data.status);
			window.location.reload(true);
        },
        error: function() {
            alert("Error occurred");
        }
    });
}

function isChristmasButtonActive() {
	let selector = '#christmas-button';
	let disable = $(selector).hasClass('disable');
	return !disable;
}

function setChristmasButtonActive(active) {
	let selector = '#christmas-button';
	if(active) $(selector).removeClass('disable');
	else $(selector).addClass('disable');
}
