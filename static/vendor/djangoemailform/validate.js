    $(document).ready(function() {
    $("#submitForm").click(function() {
        var formData = $("#myForm").serialize(); // Serialize form data
        $.ajax({
            url: "{% url 'user_contact' %}", // Replace 'your_django_view_url' with the URL of your Django view
            type: "POST",
            data: formData,
            success: function(response) {
            alert(response);
                // Handle success response
                $("#message").removeAttr("hidden");
                $("#myForm")[0].reset(); // Reset form
            },
            error: function(xhr, status, error) {
                $("#message").attr("hidden", true);
                console.error(xhr.responseText); // Log error message
                $(".error-message").html("An error occurred. Please try again later."); // Show error message
            }
        });
    });
});