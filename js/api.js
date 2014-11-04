
function update(sentence_id, level) {
	$.post("cgi/update.py", { expand: sentence_id, level: level }, function(data, response) { $("#statement-" + String(sentence_id)).replaceWith(data); });
}

