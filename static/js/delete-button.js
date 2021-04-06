$(function() {
    $('.confirm-delete').click(function(e) {
        e.preventDefault();
        if (window.confirm("Are you sure you want to delete?")) {
            location.href = $(this).data('delete-url');
        }
    });
});