

function create_issue(issue_string, callback) {
	$.post("cgi/create_issue.py", { issue: issue_string }, callback);
}
