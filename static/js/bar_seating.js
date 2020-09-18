$(document).ready(function () {
    $('#dtBasicExample').DataTable();
    $('.dataTables_length').addClass('bs-select');

    $(function () {
        $("#exporttable").click(function (e) {
            var table = $("#dtBasicExample");
            var d = new Date();

            if (table && table.length) {
                $(table).table2excel({
                    exclude: ".noExl",
                    name: "Excel Document Name",
                    filename: "Bar_Seating_" + d.getDate() + "_" + (d.getMonth()+1) + ".xls",
                    fileext: ".xls",
                    exclude_img: true,
                    exclude_links: true,
                    exclude_inputs: true,
                    preserveColors: false
                });
            }
        });

    });
});