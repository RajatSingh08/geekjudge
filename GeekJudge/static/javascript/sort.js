$(document).ready(function () {
    $('#problem_list').DataTable();
});

$(document).ready(function () {
    $('#submission_list').DataTable({
        ordering: false,
    });
});

$(document).ready(function () {
    $('#leaderboard_list').DataTable({
        ordering: false,
        "searching": false
    });
});