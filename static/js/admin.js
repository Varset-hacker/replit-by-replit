document.addEventListener('DOMContentLoaded', function() {
    // Handle menu item deletion
    const deleteButtons = document.querySelectorAll('.delete-menu-item');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Are you sure you want to delete this menu item?')) {
                const itemId = this.dataset.itemId;
                fetch(`/admin/menu/${itemId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.closest('.menu-item-row').remove();
                    }
                });
            }
        });
    });

    // Handle reservation status updates
    const statusSelects = document.querySelectorAll('.reservation-status');
    statusSelects.forEach(select => {
        select.addEventListener('change', function() {
            const reservationId = this.dataset.reservationId;
            const newStatus = this.value;
            
            fetch(`/admin/reservations/${reservationId}/status`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ status: newStatus })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.closest('tr').querySelector('.status-badge')
                        .className = `badge bg-${newStatus === 'confirmed' ? 'success' : 'warning'}`;
                }
            });
        });
    });

    // Initialize DataTables for better table management
    if (typeof $.fn.DataTable !== 'undefined') {
        $('.datatable').DataTable({
            pageLength: 10,
            responsive: true,
            order: [[0, 'desc']]
        });
    }

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});
