window.onbeforeunload = function () {
    localStorage.setItem('scrollPosition', window.scrollY);
};

function save_date() {
    const date_input_type_start = document.getElementById('date-start-type').value;
    localStorage.setItem('date_input_start_type', date_input_type_start);

    const date_input_type_end = document.getElementById('date-end-type').value;
    localStorage.setItem('date_input_end_type', date_input_type_end);

    const date_input_failure_start = document.getElementById('date-start-failure').value;
    localStorage.setItem('date_input_start_failure', date_input_failure_start);

    const date_input_failure_end = document.getElementById('date-end-failure').value;
    localStorage.setItem('date_input_end_failure', date_input_failure_end);

    const date_input_air_start = document.getElementById('date-start-air').value;
    localStorage.setItem('date_input_start_air', date_input_air_start);

    const date_input_air_end = document.getElementById('date-end-air').value;
    localStorage.setItem('date_input_end_air', date_input_air_end);
}

window.onload = function () {
    var scrollPosition = localStorage.getItem('scrollPosition');
    if (scrollPosition !== null) {
        window.scrollTo(0, scrollPosition);
    }

    var date_start_type = localStorage.getItem('date_input_start_type');
    if (date_start_type) {
        document.getElementById('date-start-type').value = date_start_type;
    }

    var date_end_type = localStorage.getItem('date_input_end_type');
    if (date_end_type) {
        document.getElementById('date-end-type').value = date_end_type;
    }

    var date_start_failure = localStorage.getItem('date_input_start_failure');
    if (date_start_failure) {
        document.getElementById('date-start-failure').value = date_start_failure;
    }

    var date_end_failure = localStorage.getItem('date_input_end_failure');
    if (date_end_failure) {
        document.getElementById('date-end-failure').value = date_end_failure;
    }

    var date_start_air = localStorage.getItem('date_input_start_air');
    if (date_start_air) {
        document.getElementById('date-start-air').value = date_start_air;
    }
    var date_end_air = localStorage.getItem('date_input_end_air');
    if (date_end_air) {
        document.getElementById('date-end-air').value = date_end_air;
    }
};