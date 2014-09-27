

function create_issue(issue_string, callback) {
	$.post("cgi/create_issue.py", { issue: issue_string }, callback);
}

function pull_issue_summaries(callback) {
	$.post("cgi/pull_issue_summaries.py", callback);
}

function pull_argument_summaries(issue_id, callback) {
	$.post("cgi/pull_argument_summaries.py", { issue: issue_id }, callback);
}

$(document).ready(function() {
	pull_issue_summaries(function(data, response) {
		$("#account_pane").append(data);
	});

});
