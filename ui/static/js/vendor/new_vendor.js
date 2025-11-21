$(document).ready(function () {
    // Initialize form handling
    initVendorForm();

    function initVendorForm() {
        const $form = $('#newVendorForm');
        const $vendorNameInput = $('#vendorName');
        const $vendorNameError = $('#vendorNameError');
        const $submitBtn = $('#submitBtn');
        let isSubmitting = false;

        // Form validation on input
        $vendorNameInput.on('input', function () {
            validateVendorName();
        });

        // Form submission handler
        $form.on('submit', function (e) {
            e.preventDefault();

            if (!validateVendorName() || isSubmitting) {
                return;
            }

            submitVendorForm();
        });

        function validateVendorName() {
            const vendorName = $vendorNameInput.val().trim();

            if (vendorName === '') {
                showError($vendorNameInput, $vendorNameError, 'Vendor name is required');
                return false;
            }

            if (vendorName.length < 2) {
                showError($vendorNameInput, $vendorNameError, 'Vendor name must be at least 2 characters long');
                return false;
            }

            if (vendorName.length > 255) {
                showError($vendorNameInput, $vendorNameError, 'Vendor name must be less than 255 characters');
                return false;
            }

            clearError($vendorNameInput, $vendorNameError);
            return true;
        }

        function showError($input, $errorElement, message) {
            $input.addClass('error').removeClass('success');
            $errorElement.text(message);
        }

        function clearError($input, $errorElement) {
            $input.removeClass('error').addClass('success');
            $errorElement.text('');
        }

        function submitVendorForm() {
            const vendorName = $vendorNameInput.val().trim();
            const formData = new FormData();
            formData.append('vendor_name', vendorName);

            setLoadingState(true);
            isSubmitting = true;

            $.ajax({
                url: '/vendor/new-vendor',
                type: 'POST',
                data: formData,
                dataType: 'json',
                processData: false, 
                contentType: false, 
                success: function (response) {
                    if (response.isSuccess) {
                        showSuccessAlert(response.message, response.url);
                    } else {
                        showErrorAlert(response.message || 'Failed to create vendor');
                    }
                },
                error: function (xhr, status, error) {
                    let errorMessage = 'An error occurred while creating the vendor';

                    try {
                        const response = JSON.parse(xhr.responseText);
                        errorMessage = response.message || errorMessage;
                    } catch (e) { }

                    showErrorAlert(errorMessage);
                },
                complete: function () {
                    setLoadingState(false);
                    isSubmitting = false;
                }
            });
        }


        function setLoadingState(loading) {
            if (loading) {
                $submitBtn.prop('disabled', true).addClass('loading');
            } else {
                $submitBtn.prop('disabled', false).removeClass('loading');
            }
        }

        function showSuccessAlert(message, redirectUrl) {
            Swal.fire({
                icon: 'success',
                title: 'Success!',
                text: message,
                timer: 5000,
                timerProgressBar: true,
                showConfirmButton: false,
                willClose: () => {
                    redirectToUrl(redirectUrl);
                }
            });

            // Fallback redirect after 5 seconds
            setTimeout(() => {
                redirectToUrl(redirectUrl);
            }, 5000);
        }

        function showErrorAlert(message) {
            Swal.fire({
                icon: 'error',
                title: 'Error!',
                text: message,
                confirmButtonText: 'OK',
                confirmButtonColor: '#667eea'
            });
        }

        function redirectToUrl(url) {
            if (url) {
                window.location.href = url;
            } else {
                // Default fallback URL
                window.location.href = '/vendor/get-all-vendors';
            }
        }

        // Handle browser back/refresh during submission
        $(window).on('beforeunload', function (e) {
            if (isSubmitting) {
                e.preventDefault();
                return 'You have unsaved changes. Are you sure you want to leave?';
            }
        });
    }
});