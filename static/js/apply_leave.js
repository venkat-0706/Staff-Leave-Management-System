document.addEventListener("DOMContentLoaded", function () {

    const duration = document.getElementById("duration");
    const sessionBox = document.getElementById("session-box");

    const startDate = document.querySelector(
        'input[name="start_date"]'
    );

    const endDate = document.querySelector(
        'input[name="end_date"]'
    );

    const leaveInfo = document.getElementById("leave-info");
    const totalDays = document.getElementById("total-days");


    // Hide Half Day Session Initially

    if (sessionBox) {
        sessionBox.style.display = "none";
    }


    // Calculate Leave Days

    function calculateLeaveDays() {

        if (
            startDate.value &&
            endDate.value &&
            duration.value === "full"
        ) {

            const start = new Date(startDate.value);
            const end = new Date(endDate.value);

            const diff =
                (end - start) /
                (1000 * 60 * 60 * 24);

            if (diff >= 0) {

                totalDays.innerHTML =
                    `📅 Total Leave Days : ${diff + 1}`;

            }

        }

        else if (
            duration.value === "half"
        ) {

            totalDays.innerHTML =
                "🕒 Total Leave Days : 0.5";

        }

        else {

            totalDays.innerHTML = "";

        }

    }


    // Start Date Change

    if (startDate && endDate) {

        startDate.addEventListener(
            "change",
            function () {

                endDate.min = startDate.value;

                if (
                    duration.value === "half"
                ) {

                    endDate.value =
                        startDate.value;

                }

                calculateLeaveDays();

            }
        );

    }


    // End Date Change

    if (endDate) {

        endDate.addEventListener(
            "change",
            calculateLeaveDays
        );

    }


    // Duration Change

    if (duration && sessionBox) {

        duration.addEventListener(
            "change",
            function () {

                if (
                    this.value === "half"
                ) {

                    sessionBox.style.display =
                        "block";

                    // Keep End Date same as Start Date

                    if (
                        startDate.value
                    ) {

                        endDate.value =
                            startDate.value;

                    }

                    // Don't disable field
                    // Just make it readonly

                    endDate.readOnly = true;

                    leaveInfo.innerHTML =
                        "🕒 Half Day Leave = 0.5 Day";

                }

                else {

                    sessionBox.style.display =
                        "none";

                    endDate.readOnly = false;

                    leaveInfo.innerHTML = "";

                }

                calculateLeaveDays();

            }
        );

    }

});