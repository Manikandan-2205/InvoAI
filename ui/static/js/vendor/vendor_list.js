$(document).ready(function () {
    let vendorsTable;
    ajax.get('/vendor/get-all-vendors-data')
        .then(response => {
            if (response.isSuccess) {              
                initializeDataTable(response.data);
            } else {
                console.error('API Error:', response.message);
            }
        })
        .catch(error => {
            console.error('Request failed:', error);

        });

    function initializeDataTable(data) {

        if ($.fn.DataTable.isDataTable('#vendorsTable')) {
            $('#vendorsTable').DataTable().destroy();
        }

        vendorsTable = $('#vendorsTable').DataTable({
            responsive: true,
            lengthChange: true,
            pageLength: 10,
            ordering: false,
            data: data,
            columns: [

                {
                    data: null,
                    className: 'sno-cell',
                    width: "50px",
                    render: function (data, type, row, meta) {
                        return meta.row + 1;
                    }
                },

                {
                    data: 'vendor_name',
                    responsivePriority: 1
                },

                {
                    data: 'created_by',
                    responsivePriority: 4,
                    render: function (data) {
                        return data || 'System';
                    }
                },
                {
                    data: 'is_active',
                    className: 'text-center',
                    render: function (data, type, row) {

                        if (row.is_deleted == 1) {
                            return '<span class="status-badge status-deleted">Deleted</span>';
                        }

                        if (row.is_deleted == 0) {
                            return '<span class="status-badge status-active">Active</span>';
                        } else {
                            return '<span class="status-badge status-inactive">Inactive</span>';
                        }
                    }
                },

                {
                    data: 'created_at',
                    className: 'created-time',
                    responsivePriority: 5,
                    render: function (data) {
                        return formatDateTime(data);
                    }
                },

                {
                    data: null,
                    responsivePriority: 2,
                    className: 'text-nowrap',
                    width: "1%",
                    render: function (data, type, row) {
                        const isDeleted = row.is_deleted || 0;
                        const disabled = isDeleted === 1 ? 'disabled' : '';


                        return `
                        <div class="action-buttons">
                            <button class="btn-action btn-view" data-id="${row.vendor_id || row.id}">
                                <i class="fas fa-eye"></i> View
                            </button>
                            <button class="btn-action btn-edit" data-id="${row.vendor_id || row.id}" ${disabled}>
                                <i class="fas fa-edit"></i> Edit
                            </button>
                            <button class="btn-action btn-delete" data-id="${row.vendor_id || row.id}" ${disabled}>
                                <i class="fas fa-trash"></i> Delete
                            </button>
                        </div>
                    `;
                    }
                }
            ],
            initComplete: function () {
                $('.dataTable thead th').css('cursor', 'default');
            },
            language: {
                emptyTable: `
                <div class="empty-state">
                    <div class="empty-state-icon"><i class="fas fa-folder-open"></i></div>
                    <h3>No Vendors Found</h3>
                    <p>Get started by adding a new vendor.</p>
                </div>
            `
            }
        });

        $('#vendorsTable').show();
    }

    $('#addVendorBtn').on('click', function () {
        window.location.href = "/vendor/new-vendor"

    });

    $(document).on('click', '#vendorsTable tbody tr', function (e) {
        if (!$(e.target).closest('.btn-action').length) {
            $(this).toggleClass('selected');

        }
    });
});

function formatDateTime(dateString) {
    if (!dateString) return 'N/A';
    try {
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return dateString;
        return date.toLocaleString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'

        });
    } catch (e) {
        return dateString;

    }
}