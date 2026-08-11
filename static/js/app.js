document.addEventListener("DOMContentLoaded", function () {

    console.log("CareerGraph application loaded successfully.");

    // Automatically hide alert messages after 5 seconds
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = "0";

            setTimeout(function () {
                alert.remove();
            }, 500);

        }, 5000);
    });

});