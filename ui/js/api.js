

function create_issue(issue_string, callback) {
	$.post("cgi/create_issue.py", { issue: issue_string }, callback);
}

function pull_issue_summaries(callback) {
	$.post("cgi/pull_issue_summaries.py", callback);
}

$(document).ready(function() {
	pull_issue_summaries(function(data, response) {

		$("#menu_pane").append(data);

	});

});
