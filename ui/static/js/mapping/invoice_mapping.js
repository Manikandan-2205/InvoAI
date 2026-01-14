$(document).ready(function () {
    ajax.get('/map/vendor-dropdown')
        .then(response => {
            if (response.isSuccess) {
                LoadVendorDropdown(response.data);
            } else {
                console.error('API Error:', response.message);
            }
        })
        .catch(error => {
            console.error('Request failed:', error);
        });

    const $mappingBody = $("#mappingBody");
    const $addRowBtn = $("#addRowBtn");

    $addRowBtn.on("click", () => {
        const rowHtml = `
      <tr>
        <td><input type="text" placeholder="field_name"></td>
        <td><input type="text" class="coord" readonly></td>
        <td><button class="btn-select">Select</button></td>
      </tr>
    `;
        $mappingBody.append(rowHtml);
    });

    $(document).on("click", ".btn-select", function () {
        const coords = "120, 80, 340, 120";
        $(this).closest("tr").find(".coord").val(coords);
    });

    $(".btn-save").on("click", () => {
        const data = [];
        $("#mappingBody tr").each(function () {
            data.push({
                field_name: $(this).find("td:eq(0) input").val(),
                coordinates: $(this).find("td:eq(1) input").val()
            });
        });

        console.log("Mapping Data:", data);
    });
});

function LoadVendorDropdown(data) {
    const $ddl = $("#ddlvendor");
    $ddl.empty();
    
    $ddl.append(new Option("Select Vendor", "", true, true));
    
    data.forEach(item => {
        const option = new Option(item.vendor_name, item.id, false, false);
        $ddl.append(option);
    });

    $ddl.select2({
        placeholder: "Select Vendor",
        allowClear: true,
        width: "100%"
    });
}
