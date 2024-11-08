document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const dateInput = document.querySelector('#date');
    const timeInput = document.querySelector('#time');
    const guestsInput = document.querySelector('#guests');

    // Set minimum date to today
    const today = new Date().toISOString().split('T')[0];
    dateInput.setAttribute('min', today);

    // Time validation
    timeInput.addEventListener('change', function() {
        const selectedTime = this.value;
        const [hours, minutes] = selectedTime.split(':');
        const time = parseInt(hours);
        
        // Restaurant hours: 11:00 - 22:00 (last reservation)
        if (time < 11 || time >= 22) {
            alert('Please select a time between 11:00 and 22:00');
            this.value = '11:00';
        }
    });

    // Guests validation
    guestsInput.addEventListener('change', function() {
        const guests = parseInt(this.value);
        if (guests < 1) {
            this.value = 1;
        } else if (guests > 20) {
            alert('For parties larger than 20, please contact us directly');
            this.value = 20;
        }
    });

    // Form validation
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    });

    // Date availability check
    dateInput.addEventListener('change', function() {
        const selectedDate = this.value;
        const selectedTime = timeInput.value;

        fetch(`/check_availability?date=${selectedDate}&time=${selectedTime}`)
            .then(response => response.json())
            .then(data => {
                if (!data.available) {
                    alert('This time slot is fully booked. Please select another time.');
                    this.value = '';
                }
            });
    });
});
