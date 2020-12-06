function toggleGraphPublic(id) {
	let active = isPublicButtonActive(id);
	setGraphPublic(id, !active);
}

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

function toggleCollation(graphid, collationid) {
	let active = isBelongsButtonActive(graphid, collationid);
	setGraphBelongsToCollation(graphid, collationid, !active);
}

function setGraphBelongsToCollation(graphid, collationid, state) {
	let method = state ? 'POST' : 'DELETE';
    $.ajax({
    	method: method,
        dataType: 'json',
        contentType: 'application/json',
        url: `/api/collations/${collationid}`,
        cache: false,
        data: JSON.stringify({'id': graphid}),
        success: function(data) {
			setBelongsButtonActive(graphid, collationid, data.present)
        },
        error: function() {
            alert("Error occurred");
        }
    });
}

function isBelongsButtonActive(graphid, collationid) {
	let selector = `#graph-${graphid}-${collationid}`;
	let disable = $(selector).hasClass('disable');
	return !disable;
}

function setBelongsButtonActive(graphid, collationid, active) {
	let selector = `#graph-${graphid}-${collationid}`;
	if(active) $(selector).removeClass('disable');
	else $(selector).addClass('disable');
}
