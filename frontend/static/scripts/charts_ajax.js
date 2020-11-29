function setGraphPublic(id, public) {
	let status = public ? 'public' : 'private';
    $.ajax({
        dataType: "json",
        url: `/api/graphs/${id}/${status}`,
        cache: false,
        success: function(data) {
			setPublicButtonActive(id, data.public);
        },
        error: function() {
            alert("Error occurred");
        }
    });
}

function toggleGraphPublic(id) {
	let active = isPublicButtonActive(id);
	setGraphPublic(id, !active);
}

function isPublicButtonActive(id) {
	let selector = `#graph-${id}-public`;
	let disable = $(selector).hasClass('disable');
	return !disable;
}

function setPublicButtonActive(id, active) {
	let selector = `#graph-${id}-public`;
	if(active) $(selector).removeClass('disable');
	else $(selector).addClass('disable');
}

function copyToClipboard(id) {
  let input = $(`#graph-${id}-url`);
  input.removeClass('d-none');
  input.select();
  document.execCommand("copy");
  input.addClass('d-none');
}
