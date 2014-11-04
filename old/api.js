

function create_issue(issue_string, callback) {
	/*$.ajax({
		type: 'POST',
		url: "cgi/create_issue.py",
		data: "issue=" + issue_string,
		beforeSend: function(XMLHttpRequest)
		{
			//Upload progress
			XMLHttpRequest.upload.addEventListener("progress", function(evt){
				if (evt.lengthComputable) {
					var percentComplete = evt.loaded / evt.total;
					//Do something with upload progress
				}
			}, false); 
			//Download progress
			
			XMLHttpRequest.addEventListener("progress", function(evt){
				if (evt.lengthComputable) {  
					var percentComplete = evt.loaded / evt.total;
					//Do something with download progress
				}
			}, false); 
		},
		success: callback);
	*/
	$.post("cgi/create_issue.py", { issue: issue_string }, callback).fail(function() { callback(); alert("error") });
}

function pull_issue_summaries(callback) {
	$.post("cgi/pull_issue_summaries.py", callback).fail(function() { callback(); alert("error") });
}

function pull_argument_summaries(issue_id, callback) {
	$('#plots').html('<img src="' + issue_id + 'flow.png" height=50%><br><img src="' + issue_id + 'subplots.png" height=50%>');	
	$.post("cgi/pull_argument_summaries.py", { issue: issue_id }, callback).fail(function() { callback(); alert("error") });
}

function pull_sentences(argument_id, callback) {
        $.post("cgi/pull_sentences.py", { argument: argument_id }, callback).fail(function() { callback(); alert("error") });
}

function update(sentence_id, issue_id) {
	$.post("cgi/update.py", { add: sentence_id, issue: issue_id}, function(data, response) { $("#issue-" + String(issue_id)).html(data); });
}

$(document).ready(function() {
	pull_issue_summaries(function(data, response) {
		$("#account_pane").append(data);
	});

});
