$(document).ready(function () {
    const canvas = document.getElementById('docCanvas');
    const ctx = canvas.getContext('2d');
    const fileInput = document.getElementById('fileInput');
    let img = new Image();
    let isDrawing = false;
    let startX, startY;
    let scaleX, scaleY;
    let currentBox = null;

    // Load vendors
    ajax.get('/map/vendor-dropdown')
        .then(response => {
            if (response.isSuccess) {
                LoadVendorDropdown(response.data);
            }
        });

    fileInput.onchange = e => {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = event => {
            img.onload = () => {
                const maxWidth = 800;
                const scale = maxWidth / img.width;
                canvas.width = maxWidth;
                canvas.height = img.height * scale;
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                
                scaleX = img.width / canvas.width;
                scaleY = img.height / canvas.height;
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
    };

    canvas.onmousedown = e => {
        const rect = canvas.getBoundingClientRect();
        startX = e.clientX - rect.left;
        startY = e.clientY - rect.top;
        isDrawing = true;
    };

    canvas.onmousemove = e => {
        if (!isDrawing) return;
        const rect = canvas.getBoundingClientRect();
        const curX = e.clientX - rect.left;
        const curY = e.clientY - rect.top;

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        
        ctx.strokeStyle = '#4a90e2';
        ctx.lineWidth = 2;
        ctx.strokeRect(startX, startY, curX - startX, curY - startY);
        
        currentBox = {
            x: Math.round(startX * scaleX),
            y: Math.round(startY * scaleY),
            w: Math.round((curX - startX) * scaleX),
            h: Math.round((curY - startY) * scaleY)
        };
    };

    canvas.onmouseup = () => {
        isDrawing = false;
        // Find the active row and update its coordinates
        const activeRow = $(".mapping-table tr.active");
        if (activeRow.length && currentBox) {
            const coordStr = JSON.stringify(currentBox);
            activeRow.find(".coord").val(coordStr);
        }
    };

    $("#addRowBtn").on("click", () => {
        const rowHtml = `
            <tr>
                <td><input type="text" class="field-name" placeholder="field_name"></td>
                <td><input type="text" class="coord" readonly></td>
                <td><button class="btn-select btn btn-sm btn-outline-primary">Target</button></td>
            </tr>
        `;
        $("#mappingBody").append(rowHtml);
    });

    $(document).on("click", ".btn-select", function () {
        $("#mappingBody tr").removeClass("active");
        $(this).closest("tr").addClass("active");
        Swal.fire({
            toast: true,
            position: 'top-end',
            icon: 'info',
            title: 'Draw a box on the image to map this field',
            showConfirmButton: false,
            timer: 3000
        });
    });

    $(".btn-save").on("click", async () => {
        const mapping = [];
        $("#mappingBody tr").each(function () {
            const field = $(this).find(".field-name").val();
            const coordVal = $(this).find(".coord").val();
            if (field && coordVal) {
                const coords = JSON.parse(coordVal);
                mapping.push({
                    label: field,
                    ...coords
                });
            }
        });

        if (mapping.length === 0) {
            Swal.fire('Error', 'No fields mapped', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('mapping', JSON.stringify(mapping));

        try {
            const response = await fetch('/map/process-ocr', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            
            if (result.success) {
                Swal.fire({
                    title: 'Extracted Results',
                    html: `<pre style="text-align: left;">${JSON.stringify(result.results, null, 2)}</pre>`,
                    icon: 'success'
                });
            } else {
                Swal.fire('Error', result.error, 'error');
            }
        } catch (error) {
            Swal.fire('Error', 'Processing failed', 'error');
        }
    });
});

function LoadVendorDropdown(data) {
    const $ddl = $("#vendorSelect");
    $ddl.empty().append(new Option("Select Vendor", "", true, true));
    data.forEach(item => $ddl.append(new Option(item.vendor_name, item.id)));
    $ddl.select2({ width: "100%" });
}
