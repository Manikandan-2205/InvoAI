$(document).ready(function() {
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

  /* Example: Setting coordinates after selecting area */
  $(document).on("click", ".btn-select", function() {
    // This should come from canvas drag selection
    const coords = "120, 80, 340, 120";
    $(this).closest("tr").find(".coord").val(coords);
  });

  /* Save Mapping */
  $(".btn-save").on("click", () => {
    const data = [];
    $("#mappingBody tr").each(function() {
      data.push({
        field_name: $(this).find("td:eq(0) input").val(),
        coordinates: $(this).find("td:eq(1) input").val()
      });
    });

    console.log("Mapping Data:", data);
  });
});
